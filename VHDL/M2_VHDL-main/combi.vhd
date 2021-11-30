LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

PACKAGE bus_mux_pkg IS
	TYPE bus_mux_array IS ARRAY(NATURAL RANGE<>) OF STD_LOGIC_VECTOR(31 DOWNTO 0);
END PACKAGE bus_mux_pkg;

----------------------------------------------

-- Mux 4->1

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity mux4_1 is
  generic (size : integer);
  port(
    reg0, reg1, reg2, reg3 : in std_logic_vector(size-1 downto 0);
    reg_out : out std_logic_vector(size-1 downto 0);
    c : in std_logic_vector(1 downto 0)
    );
end entity;

architecture arch_mux4_1 of mux4_1 is
begin
reg_out <= reg0 when c = "00"  else
           reg1 when c = "01"  else
           reg2 when c = "10"  else
           reg3;

end arch_mux4_1;

----------------------------------------------------

--Simple adder for 32 bit words

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity add is
  port(
    reg1, reg2 : in std_logic_vector(31 downto 0);
    reg3 : out std_logic_vector(31 downto 0)
    );
end entity;

architecture arch_add of add is
begin
  reg3 <= std_logic_vector(unsigned(reg1) + unsigned(reg2));
end arch_add;


------------------------------------------------------

-- 1bit adder with carry bit out

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity add1b is
  port(
    A,B,cin : in std_logic;
    s, cout : out std_logic
  );
end entity;

architecture arch_add1b of add1b is
begin
  s <= (A xor B) xor cin;
  cout <= (A and B) or (A and cin) or (B and cin);
end arch_add1b;

------------------------------------------------------

-- Full 32b adder with carry bits out

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity addCarry is
  port(
    A, B: in std_logic_vector(31 downto 0);
    cin: in std_logic;
    s : out std_logic_vector(31 downto 0);
    c30, c31: out std_logic);
end entity;



architecture arch_addCarry of addCarry is

  signal c : std_logic_vector(32 downto 0);

begin
  c(0) <= cin;
  c30 <= c(31);
  c31 <= c(32);

  G : for i in 0 to 31 generate
    inst : Entity work.add1b port map (A(i), B(i), c(i), s(i), c(i+1));
  end generate;

end arch_addCarry;

-----------------------------------------------

-- Barrel shifter

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
USE work.bus_mux_pkg.ALL;

entity BarrelShifter IS
  port (
    A : in std_logic_vector(31 downto 0);
    ValDec : in std_logic_vector(4 downto 0);
    SR, SL : out std_logic_vector(31 downto 0)
    );
end entity;

architecture arch_BarrelShifter of BarrelShifter is

signal tabSL : bus_mux_array(32 downto 0);
signal tabSR : bus_mux_array(32 downto 0);

begin

  tabSL(0) <= A;
  tabSR(0) <= A;
    
  T : for i in 1 to 32 generate
      tabSL(i) <= tabSL(i-1)(30 downto 0) & '0';
      tabSR(i) <= '0' & tabSR(i-1)(31 downto 1);
  end generate;

  SR <= tabSR(to_integer(unsigned(ValDec)));
  SL <= tabSL(to_integer(unsigned(ValDec)));

end arch_BarrelShifter;


---------------------------------------------------

-- Full ALU

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

ENTITY ALU IS
	PORT
	(
		A : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
		B : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
		sel : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		Enable_V : IN STD_LOGIC;
		ValDec : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
		Slt : IN STD_LOGIC;
		CLK : IN STD_LOGIC;
		Res : OUT STD_LOGIC_VECTOR(31 DOWNTO 0);
		N : OUT STD_LOGIC;
		Z : OUT STD_LOGIC;
		C : OUT STD_LOGIC;
		V : OUT STD_LOGIC
	);
END ENTITY ALU;


architecture arch_ALU of ALU is

  type tab8x32 is array(7 downto 0) of std_logic_vector(31 downto 0);
  signal tab : tab8x32; 

  signal c30,c31,N_int,V_int,C_int,zer : std_logic;
  signal SR,SL,S,bufferRes,zero : std_logic_vector(31 downto 0);

begin

  addC : Entity work.addCarry port map (A, B, sel(3), S, c30, c31);
  barrelSh : Entity work.BarrelShifter port map (B, ValDec,SR,SL);
  zero <= (others => '0');
  tab(0) <= A and B;
  tab(1) <= A or B;
  tab(2) <= S;
  tab(3) <= (0 => (Enable_V and (N_int xor V_int)) or ((not Enable_V) and C_int), others => '0');
  tab(4) <= A nor B;
  tab(5) <= A xor B;
  tab(6) <= SR;
  tab(7) <= SL;

  bufferRes <= tab(to_integer(unsigned(sel(2 downto 0))));
  Res <= bufferRes;

  zer <= '0' when bufferRes = zero else
         '1';

P_ALU : process(CLK)

  begin
    if (CLK'event and CLK ='0') then 
      C_int <= sel(3) xor c31;
      C <= sel(3) xor c31;

      V_int <= Enable_V and (not Slt) and (c31 xor c30);
      V <= Enable_V and (not Slt) and (c31 xor c30);

      N_int <= S(31);
      N <= S(31);

      Z <= zer;
      
    end if;
  end process P_ALU;

end arch_ALU;

---------------------------------------------------

-- Extension logic for immediate inputs

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity extension is
  port(
    inst : in std_logic_vector(31 downto 0);
    ExtOp : in std_logic;
    ExtOut : out std_logic_vector(31 downto 0)
    );
end entity;

architecture arch_extension of extension is
  signal zero,b15 : std_logic_vector(15 downto 0);
begin
  zero <= (others => '0');
  b15 <= (others => inst(15));
  ExtOut <= zero & inst(15 downto 0) when ExtOp = '0' else 
            b15 & inst(15 downto 0) when ExtOp = '1';

end arch_extension;