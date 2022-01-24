LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

----------------------------------------------

-- R3000

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity R3000 is
    port(
        CLK, WE : in std_logic
    );
end entity;

architecture arch_R3000 of R3000 is
    
    signal instr, ext , PC, A, B, data_i, ResALU, data_0_1, data, mixte, filler32 : std_logic_vector(31 downto 0);
    signal dest_reg, ValDec : std_logic_vector(4 downto 0);
    signal Sel : std_logic_vector(3 downto 0);
    signal MemToReg, RegDst, UAL_Src, UAL_Op, Jump : std_logic_vector (1 downto 0);
    signal OpExt, WR_Reg, B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gez, B_gez_AI, B_itz_AI, EcrireMem_W, EcrireMem_H, EcrireMem_B, LireMem_W, LireMem_SH, LireMem_UH, LireMem_SB, LireMem_UB, Slt_slti, Enable_V, N, Z, C, V, CPSrc : std_logic;
begin
    filler32 <= (others => '0');

    InstrMem : Entity work.memoire port map (PC, filler32, instr, '1','0','0','0','0','0','0','0','1','0',CLK);

    Decodeur : Entity work.decodeur port map (instr(31 downto 26), MemToReg, RegDst, UAL_Src, UAL_Op, Jump,OpExt, WR_Reg, B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gez, B_gez_AI, B_itz_AI, EcrireMem_W, EcrireMem_H, EcrireMem_B, LireMem_W, LireMem_SH, LireMem_UH, LireMem_SB, LireMem_UB);
    
    Extension : Entity work.extension port map (instr, OpExt, ext);

    MuxPreReg : Entity work.mux4_1 generic map(5) port map(instr(20 downto 16), instr(15 downto 11), "11111","11111",dest_reg, RegDst);
    RegBank : Entity work.RegisterBank port map(instr(25 downto 21), A, instr(20 downto 16), data_0_1, dest_reg, data_i, WR_Reg, CLK);
    mixte(31 downto 16) <= (others => '0');
    mixte(15 downto 0) <= instr(15 downto 0);
    MuxPostReg : Entity work.mux4_1 generic map(32) port map(data_0_1, ext, filler32, mixte, B, UAL_Src);

    ALU_Ctrl : Entity work.ALU_Control port map(UAL_Op,instr(5 downto 0), instr(31 downto 26), Sel, Slt_slti, Enable_V); 
    ALU : Entity work.ALU port map(A, B, Sel, Enable_V, ValDec,Slt_slti, CLK, ResALU, N, Z, C, V );

    PC_Ctrl : Entity work.PC_Control port map(N, Z, B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gez, B_gez_AI, B_itz_AI, instr(16), CPSrc);

    DataMem : Entity work.memoire port map (data_0_1, ResALU, data, LireMem_W, LireMem_SH, LireMem_UH, LireMem_SB, LireMem_UB, EcrireMem_W, EcrireMem_H, EcrireMem_B, WE, '0', CLK);

end arch_R3000;