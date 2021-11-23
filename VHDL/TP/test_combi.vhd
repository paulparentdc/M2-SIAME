LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

-------------------------------------------------

-- Register
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_mux4_1 is 
end test_mux4_1;

architecture arch_test_mux4_1 of test_mux4_1 is 

signal reg0, reg1, reg2, reg3 : std_logic_vector(3 downto 0);
signal reg_out                : std_logic_vector(3 downto 0);
signal c                      : std_logic_vector(1 downto 0);

-- definition de constantes
constant clkpulse : Time := 5 ns; -- 1/2 periode horloge

begin

-- mapping des composants du registre
regmap:entity	work.mux4_1(arch_mux4_1)
    generic map(4)
	port map(reg0, reg1, reg2, reg3, reg_out, c);

-- debut sequence de test
REG_TEST : process
begin
	wait for clkpulse;
	reg0<="0000";
    reg1<="0001";
    reg2<="0011";
    reg3<="0111";
    c<="00";
	wait for clkpulse;
	c<="01";
	wait for clkpulse;
	c<="10";
	wait for clkpulse;

	-- LATEST COMMAND (NE PAS ENLEVER !!!)
	wait for clkpulse/2;
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;

end process REG_TEST;
end arch_test_mux4_1;
-------------------------------------------------

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_BarrelShifter is 
end test_BarrelShifter;

architecture arch_test_BarrelShifter of test_BarrelShifter is 

signal A      : std_logic_vector(31 downto 0);
signal ValDec : std_logic_vector(4 downto 0);
signal SR, SL : std_logic_vector(31 downto 0);

-- definition de constantes
constant clkpulse : Time := 5 ns; -- 1/2 periode horloge

begin

-- mapping des composants du registre
regmap:entity work.BarrelShifter
	port map(A, ValDec, SR, SL);

-- debut sequence de test
REG_TEST : process
begin
	wait for clkpulse;
	A<=(16=>'1', others=>'0');
    ValDec<="00100";
	wait for clkpulse;
	ValDec<="00001";
	wait for clkpulse;

	-- LATEST COMMAND (NE PAS ENLEVER !!!)
	wait for clkpulse/2;
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;

end process REG_TEST;
end arch_test_BarrelShifter;
-------------------------------------------------
-------------------------------------------------
