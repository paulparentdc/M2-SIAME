LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_extension is
end test_extension;
    
-- Definition de l'architecture
architecture arch_test_extension of test_extension is

-- definition de ressources externes

signal E_inst, E_ExtOut : std_logic_vector(31 downto 0);
signal E_ExtOp : std_logic;


begin
--------------------------
-- definition de l'horloge


regf0 : entity work.extension(arch_extension)
    port map(inst => E_inst, ExtOp => E_ExtOp, ExtOut => E_ExtOut);

P_Test: process
begin

    E_inst <= (others => '1');
    E_ExtOp <= '0';
    wait for 5 ns;

    E_inst <= (15 => '1',31 => '1', others => '0');
    E_ExtOp <= '1';
    wait for 5 ns;

    E_ExtOp <= '0';
    wait for 5 ns;

    E_ExtOp <= '1';
    wait for 5 ns;

	wait;

end process P_Test;

end arch_test_extension;