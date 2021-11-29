LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_ALU is
end test_ALU;
    
-- Definition de l'architecture
architecture arch_test_ALU of test_ALU is

-- definition de ressources externes

signal E_A, E_B, E_Res: std_logic_vector(31 downto 0);
signal E_sel: std_logic_vector(3 downto 0);
signal E_ValDec: std_logic_vector(4 downto 0);
signal E_Enable_V, E_Slt, E_CLK, E_N, E_Z, E_C, E_V: std_logic;



begin


regf0 : entity work.ALU(arch_ALU)
    port map(A => E_A,
        B => E_B,
        sel => E_sel,
        Enable_V => E_Enable_V,
        ValDec => E_ValDec, 
        Slt => E_Slt,
        CLK => E_CLK,
        Res => E_Res,
        N => E_N,
        Z => E_Z,
        C => E_C,
        V => E_V);

P_Test: process
begin
    E_CLK <= '1';
    E_Enable_V <= '0';
    E_ValDec <= "00001";
    E_Slt <= '0';

    
    E_sel <= "0000"; -- And
    E_A <= (0 => '1',1 => '1', 2 => '1', 3 => '1' ,others => '0');
    E_B <= (0 => '0',1 => '0', 2 => '0', 3 => '0' ,others => '1');
    wait for 5 ns;

    E_CLK <= '0';
    E_sel <= "0001"; -- Or

    wait for 5 ns;

    E_CLK <= '1';
    E_sel <= "0010"; -- AddCarry

    wait for 5 ns;

    E_CLK <= '0';
    E_sel <= "0011"; -- Positionner si inferieur

    wait for 5 ns;

    E_CLK <= '1';
    E_sel <= "0100"; -- nor

    wait for 5 ns;

    E_CLK <= '0';
    E_sel <= "0101"; -- xor


    wait for 5 ns;

    E_A <= (31 => '0', others => '1');
    E_B <= (others => '1');
    E_CLK <= '1';
    E_sel <= "0101"; -- add

    wait for 5 ns;

    E_CLK <= '0';
    E_sel <= "0011"; -- Positionner si inferieur

    wait for 5 ns;
	wait;

end process P_Test;

end arch_test_ALU;