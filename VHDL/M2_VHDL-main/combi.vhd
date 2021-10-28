
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
  s <= A xor B;
  cout <= A and B;
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

  component add1b
    port(
      A,B,cin : in std_logic;
      cout, s : out std_logic
    );
  end component;

  signal c : std_logic_vector(32 downto 0);

begin
  c(0) <= cin;
  c30 <= c(31);
  c31 <= c(32);

  G : for i in 0 to 31 generate
    inst : add1b port map (A(i), B(i), c(i), s(i), c(i+1));
  end generate;

end arch_addCarry;


-----------------------------------------------

-- Barrel shifter

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
use work.bus_mux_pkg.ALL;

entity BarrelShifter IS
  port (
    A : in std_logic_vector(31 downto 0);
    ValDec : in std_logic_vector(4 downto 0);
    SR, SL : out std_logic_vector(31 downto 0)
    );
end entity;

architecture arch_BarrelShifter of BarrelShifter is
  --type Tab32 is array(0 to 31) of std_logic_vector(31 downto 0);
  --signal tabSL : Tab32;
  --signal tabSR : Tab32;

begin


  SR <= shift_right(A,to_integer(unsigned(ValDec)));
  SL <= shift_left(A,to_integer(unsigned(ValDec)));
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
