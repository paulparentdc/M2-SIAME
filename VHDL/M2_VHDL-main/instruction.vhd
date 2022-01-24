LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

----------------------------------------------

-- Décodeur op

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity decodeur is
    port(
        ln : in std_logic_vector(5 downto 0);
        MemToReg, RegDst, UAL_Src, UAL_Op, Jump : out std_logic_vector(1 downto 0);
        OpExt, WR_Reg, B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gez, B_gez_AI, B_itz_AI, EcrireMem_W, EcrireMem_H, EcrireMem_B, LireMem_W, LireMem_SH, LireMem_UH, LireMem_SB, LireMem_UB : out std_logic
    );
end entity;

architecture arch_decodeur of decodeur is
    signal minterms : std_logic_vector(63 downto 0);
begin
    minterms(0) <= '1' when ln(5 downto 0) = "000000" else '0';
    minterms(1) <= '1' when ln(5 downto 0) = "000001" else '0';
    minterms(2) <= '1' when ln(5 downto 0) = "000010" else '0';
    minterms(3) <= '1' when ln(5 downto 0) = "000011" else '0';
    minterms(4) <= '1' when ln(5 downto 0) = "000100" else '0';
    minterms(5) <= '1' when ln(5 downto 0) = "000101" else '0';
    minterms(6) <= '1' when ln(5 downto 0) = "000110" else '0';
    minterms(7) <= '1' when ln(5 downto 0) = "000111" else '0';
    minterms(8) <= '1' when ln(5 downto 0) = "001000" else '0';
    minterms(9) <= '1' when ln(5 downto 0) = "001001" else '0';
    minterms(10) <= '1' when ln(5 downto 0) = "001010" else '0';
    minterms(11) <= '1' when ln(5 downto 0) = "001011" else '0';
    minterms(12) <= '1' when ln(5 downto 0) = "001100" else '0';
    minterms(13) <= '1' when ln(5 downto 0) = "001101" else '0';
    minterms(14) <= '1' when ln(5 downto 0) = "001110" else '0';
    minterms(15) <= '1' when ln(5 downto 0) = "001111" else '0';
    minterms(16) <= '1' when ln(5 downto 0) = "010000" else '0';
    minterms(17) <= '1' when ln(5 downto 0) = "010001" else '0';
    minterms(18) <= '1' when ln(5 downto 0) = "010010" else '0';
    minterms(19) <= '1' when ln(5 downto 0) = "010011" else '0';
    minterms(20) <= '1' when ln(5 downto 0) = "010100" else '0';
    minterms(21) <= '1' when ln(5 downto 0) = "010101" else '0';
    minterms(22) <= '1' when ln(5 downto 0) = "010110" else '0';
    minterms(23) <= '1' when ln(5 downto 0) = "010111" else '0';
    minterms(24) <= '1' when ln(5 downto 0) = "011000" else '0';
    minterms(25) <= '1' when ln(5 downto 0) = "011001" else '0';
    minterms(26) <= '1' when ln(5 downto 0) = "011010" else '0';
    minterms(27) <= '1' when ln(5 downto 0) = "011011" else '0';
    minterms(28) <= '1' when ln(5 downto 0) = "011100" else '0';
    minterms(29) <= '1' when ln(5 downto 0) = "011101" else '0';
    minterms(30) <= '1' when ln(5 downto 0) = "011110" else '0';
    minterms(31) <= '1' when ln(5 downto 0) = "011111" else '0';
    minterms(32) <= '1' when ln(5 downto 0) = "100000" else '0';
    minterms(33) <= '1' when ln(5 downto 0) = "100001" else '0';
    minterms(34) <= '1' when ln(5 downto 0) = "100010" else '0';
    minterms(35) <= '1' when ln(5 downto 0) = "100011" else '0';
    minterms(36) <= '1' when ln(5 downto 0) = "100100" else '0';
    minterms(37) <= '1' when ln(5 downto 0) = "100101" else '0';
    minterms(38) <= '1' when ln(5 downto 0) = "100110" else '0';
    minterms(39) <= '1' when ln(5 downto 0) = "100111" else '0';
    minterms(40) <= '1' when ln(5 downto 0) = "101000" else '0';
    minterms(41) <= '1' when ln(5 downto 0) = "101001" else '0';
    minterms(42) <= '1' when ln(5 downto 0) = "101010" else '0';
    minterms(43) <= '1' when ln(5 downto 0) = "101011" else '0';
    minterms(44) <= '1' when ln(5 downto 0) = "101100" else '0';
    minterms(45) <= '1' when ln(5 downto 0) = "101101" else '0';
    

    MemToReg(1) <= minterms(0) or minterms(1) or minterms(3);
    MemToReg(0) <= minterms(32) or minterms(32) or minterms(35) or minterms(36) or minterms(37);

    OpExt <= minterms(1) or minterms(4) or minterms(5) or minterms(6) or minterms(7) or minterms(8) or minterms(10) or minterms(32) or minterms(32) or minterms(35) or minterms(36) or minterms(37) or minterms(40) or minterms(41) or minterms(43);

    RegDst(0) <= minterms(0);
    RegDst(1) <= minterms(1) or minterms(3);
    
    WR_Reg <= minterms(0) or minterms(1) or minterms(3) or minterms(8) or minterms(9) or minterms(10) or minterms(11) or minterms(12) or minterms(13) or minterms(14) or minterms(15) or minterms(32) or minterms(33) or minterms(35) or minterms(36) or minterms(37);  

    UAL_Src(0) <= minterms(8) or minterms(9) or minterms(10) or minterms(11) or minterms(12) or minterms(13) or minterms(14) or minterms(15);
    UAL_Src(1) <= minterms(1) or  minterms(15);

    UAL_Op(0) <= minterms(1) or minterms(4) or minterms(5) or minterms(6) or minterms(7) or minterms(8) or minterms(9) or minterms(10) or minterms(11) or minterms(12) or minterms(13) or minterms(14) or minterms(15);
    UAL_Op(1) <= minterms(0) or minterms(8) or minterms(9) or minterms(10) or minterms(11) or minterms(12) or minterms(13) or minterms(14) or minterms(15);

    B_eq <= minterms(4);
    B_ne <= minterms(5);
    B_lez <= minterms(6);
    B_gtz <= minterms(7);
    B_bltz <= minterms(1);
    B_gez <= minterms(1);
    B_gez_AI <= minterms(1);
    B_itz_AI <= minterms(1);

    EcrireMem_W <= minterms(43);
    EcrireMem_H <= minterms(41);
    EcrireMem_B <= minterms(40);

    LireMem_W <= minterms(35);
    LireMem_SH <= minterms(33);
    LireMem_UH <= minterms(37);
    LireMem_SB <= minterms(32);
    LireMem_UB <= minterms(36);

    Jump(0) <= minterms(2) or minterms(3);
    Jump(1) <= minterms(0); 

end arch_decodeur;


----------------------------------------------

-- ALU Control

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity ALU_Control is
  port(
    UAL_Op : in std_logic_vector(1 downto 0);
    F, Op : in std_logic_vector(5 downto 0);
    Sel : out std_logic_vector(3 downto 0);
    Slt_slti, Enable_V : out std_logic
    );
end entity;

architecture arch_ALU_Control of ALU_Control is
begin

Sel(0) <= '1' when (((UAL_OP(1) = '1' and UAL_OP(0) ='0') and 
          ((F(5)='0' and F(3 downto 0) = "0000") or (F(5)='1' and F(3 downto 0) = "1010")  or (F(5)='0' and F(3 downto 0) = "0110") or (F(5)='0' and F(3 downto 1) = "101"))) or
          ( UAL_OP(1) = '1' and UAL_OP(0) ='1' and (Op(1) = '1' or (Op(2) = '1' and Op(1) = '0' and Op(0) = '0') ) ))
          else '0';

Sel(1) <= '1' when ( UAL_OP(1) = '0' or ( UAL_OP(1) = '1' and UAL_OP(0) = '0' and ( (F(3 downto 2) = "00" and F(0) = '0') or (F(5)='0' and F(3 downto 0) = "0100") or (F(5)='0' and F(3 downto 0) = "1001") or (F(5)='1' and F(3 downto 2) = "00" and F(0)='1') or (F(5)='0' and F(3 downto 0) = "101") ) )
          or ( UAL_OP(1 downto 0) = "11" and Op(2) = '0') ) 
          else '0' ;
          
Sel(2) <= '1' when ( (UAL_OP(1 downto 0) = "10" and ( (F(5)='0' and F(3 downto 2) = "00" and F(0)='0') or (F(5)='0' and F(3 downto 1) = "011") ))
          or (UAL_OP(1 downto 0) = "11" and Op(2 downto 0) = "110") )
          else '0';

Sel(3) <= '1' when  ( (UAL_OP(1 downto 0) = "01") or ( UAL_OP(1 downto 0) = "10" and ( (F(5)='1' and F(3 downto 1) = "001") or (F(5)='0' and F(3 downto 1) = "101") ) )
          or (UAL_OP(1 downto 0) = "11" and Op(2 downto 1) = "01") )
          else '0';

Slt_slti <= '1' when  ( (UAL_OP(1 downto 0) = "10" and  F(3 downto 0) = "1010") or ( UAL_OP(1 downto 0) = "11" and Op(2 downto 0) = "010" ) )
          else '0';

Enable_V <= '1' when  ( (UAL_OP(1 downto 0) = "10" and F(5) = '1' and F(2) = '0' and F(0) = '0') or ( UAL_OP(1 downto 0) = "00" ) )
          else '0';

end arch_ALU_Control;




----------------------------------------------

-- PC_Control

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity PC_Control is
  port(
    N, Z, B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gez, B_gez_AI, B_itz_AI, rt0 : in std_logic;
    CPSrc : out std_logic
    );
end entity;

architecture arch_PC_Control of PC_Control is
begin
    CPSrc <= '1' when ( (B_eq = '1' and Z = '1') or (B_ne = '1' and Z = '0') or (B_lez = '1' and (N = '1' or Z = '1')) or (B_gtz = '1' and N = '0' and Z = '0')
                 or (B_bltz = '1' and N = '1' and Z = '0') or (B_gez = '1' and (N = '0' or Z = '1')) or ( B_itz_AI = '1' and rt0 = '0' and N = '1' and Z = '0') or ( B_gez_AI = '1' and rt0 = '1' and (N = '0' or Z = '1') )  ) 
                 else '0';           
end arch_PC_Control;