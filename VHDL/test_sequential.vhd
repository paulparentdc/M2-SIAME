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

