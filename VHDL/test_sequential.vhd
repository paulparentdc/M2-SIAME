LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

-------------------------------------------------

-- Register

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_Reg is 
end test_Reg;

architecture arch_test_Reg of test_Reg is 

signal S      : std_logic_vector(31 downto 0);
signal OUTPUT : std_logic_vector(31 downto 0);
signal WR     : std_logic;
signal E_CLK    : std_logic;

-- definition de constantes
constant clkpulse : Time := 5 ns; -- 1/2 periode horloge

begin

-- definition de l'horloge
P_E_CLK: process
begin
	E_CLK <= '1';
	wait for clkpulse;
	E_CLK <= '0';
	wait for clkpulse;
end process P_E_CLK;

-- mapping des composants du registre
reg0:entity	work.Reg
	port map(S, OUTPUT, WR, E_CLK);

-- debut sequence de test
REG_TEST : process
begin
	wait for clkpulse;
	S<=(0=>'1',3=>'1',others=>'0');
	WR<='1';
	wait for clkpulse;
	S<=(0=>'1',others=>'0');
	WR<='0';
	wait for clkpulse;
	S<=(4=>'1',others=>'0');
	WR<='1';
	wait for clkpulse;

	-- LATEST COMMAND (NE PAS ENLEVER !!!)
	wait until (rising_edge(E_CLK)); wait for clkpulse/2;
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;

end process REG_TEST;
end arch_test_Reg;
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_RegBank is 
end test_RegBank;

architecture arch_test_RegBank of test_RegBank is 

signal s_reg_0  : STD_LOGIC_VECTOR(4 DOWNTO 0);
signal data_o_0 : STD_LOGIC_VECTOR(31 DOWNTO 0);
signal s_reg_1  : STD_LOGIC_VECTOR(4 DOWNTO 0);
signal data_o_1 :  STD_LOGIC_VECTOR(31 DOWNTO 0);
signal dest_reg : STD_LOGIC_VECTOR(4 DOWNTO 0);
signal data_i   :  STD_LOGIC_VECTOR(31 DOWNTO 0);
signal wr_reg   : STD_LOGIC;
signal clk      : STD_LOGIC;

-- definition de constantes
constant clkpulse : Time := 5 ns; -- 1/2 periode horloge

begin

-- definition de l'horloge
P_CLK: process
begin
	clk <= '1';
	wait for clkpulse;
	clk <= '0';
	wait for clkpulse;
end process P_CLK;

-- mapping des composants du registre
regBank0:entity	work.RegisterBank
	port map(s_reg_0, data_o_0, s_reg_1, data_o_1,dest_reg, data_i, data_i, wr_reg, clk);

-- debut sequence de test
REGBANK_TEST : process
begin
	wait for clkpulse;
	S<=(0=>'1',3=>'1',others=>'0');
	WR<='1';
	wait for clkpulse;
	S<=(0=>'1',others=>'0');
	WR<='0';
	wait for clkpulse;
	S<=(4=>'1',others=>'0');
	WR<='1';
	wait for clkpulse;

	-- LATEST COMMAND (NE PAS ENLEVER !!!)
	wait until (rising_edge(clk)); wait for clkpulse/2;
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;

end process REGBANK_TEST;
end arch_test_RegBank;

