LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_barrel is
end test_barrel;
    
-- Definition de l'architecture
architecture arch_test_barrel of test_barrel is

-- definition de ressources externes

signal E_A, E_SR, E_SL: std_logic_vector(31 downto 0);
signal E_ValDec : std_logic_vector(4 downto 0);


begin
--------------------------
-- definition de l'horloge


regf0 : entity work.BarrelShifter(arch_BarrelShifter)
    port map(A => E_A, ValDec => E_ValDec, SR => E_SR, SL => E_SL);

P_Test: process
begin

    E_A <= (others => '1');
    E_ValDec <= "00001";
    wait for 5 ns;

    E_ValDec <= "00011";
    wait for 5 ns;

    E_ValDec <= "00000";
    wait for 5 ns;

    E_ValDec <= "11111";
    wait for 5 ns;

	wait;

end process P_Test;

end arch_test_barrel;