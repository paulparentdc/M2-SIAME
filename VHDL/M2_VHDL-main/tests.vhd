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

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;


-- Definition de l'entite
entity test_barrel is
end test_barrel;
    
-- Definition de l'architecture
architecture arch_test_barrel of test_barrel is

-- definition de ressources externes

    signal E_A : std_logic_vector(31 downto 0);
    signal E_ValDec : std_logic_vector(4 downto 0);
    signal E_SR, E_SL : std_logic_vector(31 downto 0);



begin
--------------------------
-- definition de l'horloge


regf0 : entity work.BarrelShifter(arch_BarrelShifter)
    port map(A => E_A, ValDec => E_ValDec, SR => E_SR, SL => E_SL);

P_Test: process
begin

    E_A <= (others => '1');
    E_ValDec <= (0 => '1', others => '0');

    wait for 5 ns;

    E_A <= (others => '1');
    E_ValDec <= (others => '0');

    wait for 5 ns;

    E_A <= (others => '1');
    E_ValDec <= (3 => '1', others => '0');

    wait for 5 ns;

    E_A <= (others => '1');
    E_ValDec <= (3 => '1', others => '0');

    wait for 5 ns;

    E_A <= (others => '1');
    E_ValDec <= (others => '1');  
    
    wait for 5 ns;
    
	wait;

end process P_Test;

end arch_test_barrel;





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


