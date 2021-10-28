LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_add is
end test_add;
    
-- Definition de l'architecture
architecture arch_test_add of test_add is

-- definition de ressources externes

signal E_reg1, E_reg2, E_reg3: std_logic_vector(31 downto 0);



begin
--------------------------
-- definition de l'horloge


regf0 : entity work.add(arch_add)
    port map(reg1 => E_Reg1, reg2 => E_reg2, reg3 => E_reg3);

P_Test: process
begin

    E_Reg1 <= (others => '0');
    E_Reg2 <= (0 => '1', others => '0');

    wait for 5 ns;

    E_Reg1 <= (0 => '1', others => '0');
    E_Reg2 <= (0 => '1', others => '0');

    wait for 5 ns;

    E_Reg1 <= (0 => '1', others => '0');
    E_Reg2 <= (1 => '1', others => '0');
    wait for 5 ns;

	wait;

end process P_Test;

end arch_test_add;