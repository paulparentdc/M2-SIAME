LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_addCarry is
end test_addCarry;
    
-- Definition de l'architecture
architecture arch_test_addCarry of test_addCArry is

-- definition de ressources externes

signal E_A, E_B, E_S: std_logic_vector(31 downto 0);
signal E_cin, E_C31, E_c30 : std_logic;


begin
--------------------------
-- definition de l'horloge


regf0 : entity work.addCarry(arch_addCarry)
    port map(A => E_A, B => E_B, cin => E_cin, s => E_s, c31 => E_c31, c30 => E_c30);

P_Test: process
begin

    E_A <= (others => '1');
    E_B <= (others => '1');
    E_cin <= '0';
    
    wait for 5 ns;

    E_A <= (0 => '1' , others => '0');
    E_B <= (0 => '0' , others => '1');
    E_cin <= '0';

    wait for 5 ns;

    E_A <= (others => '0');
    E_B <= (others => '0');
    E_cin <= '1';
    
	wait;

end process P_Test;

end arch_test_addCarry;