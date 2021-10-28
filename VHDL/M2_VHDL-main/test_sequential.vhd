LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

-------------------------------------------------

-- Register

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_registres is
end test_registres;
    
-- Definition de l'architecture
architecture arch_test_reg of test_registres is

-- definition de ressources externes
signal E_CLK,E_WR						: std_logic;
signal S,O                                : std_logic_vector(31 downto 0);

constant clkpulse : Time := 5 ns; -- 1/2 periode horloge

begin
--------------------------
-- definition de l'horloge
P_E_CLK: process
begin
	E_CLK <= '1';
	wait for clkpulse;
	E_CLK <= '0';
	wait for clkpulse;
end process P_E_CLK;


regf0 : entity work.reg(arch_reg)
    port map(CLK => E_CLK, source => S, output => O, wr => E_WR);


P_Test: process
begin

    S <= (others=>'0');
    E_WR <= '1';

    wait until (rising_edge(E_CLK)); wait for clkpulse/2;
    S <= (others=>'1');
    E_WR <= '0';

    wait until (rising_edge(E_CLK)); wait for clkpulse/2;
    S <= (1 => '0', others=>'1');
    E_WR <= '1';

    wait until (rising_edge(E_CLK)); wait for clkpulse/2;
    


    
    -- LATEST COMMAND (NE PAS ENLEVER !!!)
	wait until (rising_edge(E_CLK)); wait for clkpulse/2;
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;
end process P_Test;

end arch_test_reg;