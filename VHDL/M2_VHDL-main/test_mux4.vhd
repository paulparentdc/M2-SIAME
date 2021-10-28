LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_mux is
end test_mux;
    
-- Definition de l'architecture
architecture arch_test_mux of test_mux is

-- definition de ressources externes

signal E_reg0, E_reg1, E_reg2, E_reg3, E_reg_out : std_logic_vector(3 downto 0);
signal E_c : std_logic_vector(1 downto 0);


begin
--------------------------
-- definition de l'horloge


regf0 : entity work.mux4_1(arch_mux4_1)
    generic map(4)
    port map(reg0 => E_reg0 ,reg1 => E_reg1,reg2 => E_reg2,reg3 => E_reg3, reg_out => E_reg_out, c => E_c);

P_Test: process
begin
    
    E_reg0 <= "0000";
    E_reg1 <= "0001";
    E_reg2 <= "0010";
    E_reg3 <= "0011";
    E_C <= "00";
    wait for 5 ns;
    E_C <= "01";
    wait for 5 ns;
    E_C <= "10";
    wait for 5 ns;
    E_C <= "11";
    wait for 5 ns;
    
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;

end process P_Test;

end arch_test_mux;