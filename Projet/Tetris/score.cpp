int Game::computeScore(int nbLinesDeleted)
{
    int level = getLevel(); // Le niveau actuel
    int score = 0;
 
    switch(nbLinesDeleted)
    {
        case 1:
            score = 40 * (level + 1);
            break;
        case 2:
            score = 100 * (level + 1);
            break;
        case 3:
            score = 300 * (level + 1);
            break;
        case 4:
             score = 1200 * (level + 1);
             break;
         default:
             break;
    }
 
    return score;
}