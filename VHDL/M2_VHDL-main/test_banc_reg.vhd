
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_banc_registres is
end test_banc_registres;
    
-- Definition de l'architecture
architecture arch_test_banc_reg of test_banc_registres is

-- definition de ressources externes
signal E_s_reg_0 : std_logic_vector(4 downto 0) := "00000";
signal E_s_reg_1 : std_logic_vector(4 downto 0) := "00001";
signal E_dest_reg : std_logic_vector(4 downto 0);
signal E_CLK,E_WR : std_logic;
signal E_data_i : std_logic_vector(31 downto 0);
signal E_data_o_0 : std_logic_vector(31 downto 0);
signal E_data_o_1 : std_logic_vector(31 downto 0);

constant clkpulse : Time := 5 ns; -- 1/2 periode horloge

begin
--------------------------
-- definition de l'horloge



regf0 : entity work.RegisterBank
    port map(s_reg_0 => E_s_reg_0, data_o_0 => E_data_o_0, s_reg_1 =>  E_s_reg_1, data_o_1 => E_data_o_1, dest_reg => E_dest_reg, data_i => E_data_i, wr_reg => E_WR, clk => E_CLK);

P_Test: process
begin
    E_CLK <= '0';
    E_WR <= '0';
    E_data_i <= (others => '1');
    wait for 5 ns;

    E_CLK <= '1';
    E_WR <= '1';
    E_data_i <= (others => '1');
    E_dest_reg <= (others => '1');
    wait for 5 ns;

    E_CLK <= '0';
    E_WR <= '1';
    E_data_i <= (others => '1');
    E_s_reg_0 <= (others => '1');
    wait for 5 ns;

    E_CLK <= '1';
    E_WR <= '1';
    E_data_i <= (0 => '0' ,others => '1');
    E_dest_reg <= (others => '1');
    wait for 5 ns;
    



 
	assert FALSE report "FIN DE SIMULATION" severity FAILURE;

end process P_Test;

end arch_test_banc_reg;
