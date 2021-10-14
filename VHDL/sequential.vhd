LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

PACKAGE bus_mux_pkg IS
	TYPE bus_mux_array IS ARRAY(NATURAL RANGE<>) OF STD_LOGIC_VECTOR(31 DOWNTO 0);
END PACKAGE bus_mux_pkg;

-------------------------------------------------

-- Register

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Reg is
  PORT(
    source: in std_logic_vector(31 downto 0);
    output : out std_logic_vector(31 downto 0);
    wr, clk : in std_logic
    );
end entity;

architecture arch_Reg of Reg is 
begin
	process(clk)
	begin
		if(rising_edge(CLK)) then
			if(wr='1') then
				output<=source;
			end if;
		end if;
	end process;
end arch_Reg;

-------------------------------------------------

-- Register bank

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
USE work.bus_mux_pkg.ALL;

ENTITY RegisterBank IS
	PORT
	(
		s_reg_0 : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
		data_o_0 : OUT STD_LOGIC_VECTOR(31 DOWNTO 0);
		s_reg_1 : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
		data_o_1 : OUT STD_LOGIC_VECTOR(31 DOWNTO 0);
		dest_reg : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
		data_i : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
		wr_reg : IN STD_LOGIC;
		clk : IN STD_LOGIC
	);
END ENTITY RegisterBank;
