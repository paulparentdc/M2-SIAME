def decomp(n):
    L = dict()
    k = 2
    while n != 1:
        exp = 0
        while n % k == 0:
            n = n // k
            exp += 1
        if exp != 0:
            L[k] = exp
        k = k + 1
        
    return L


def _ppcm(a,b):
    Da = decomp(a)
    Db = decomp(b)
    p = 1
    for facteur , exposant in Da.items():
        if facteur in Db:
            exp = max(exposant , Db[facteur])
        else:
            exp = exposant
        
        p *= facteur**exp
        
    for facteur , exposant in Db.items():
        if facteur not in Da:
            p *= facteur**exposant
            
    return p


def ppcm(L):
    if len(L) == 2:
        return _ppcm(L[0],L[1])
    else:
        n = len(L)
        i = 0
        A = []
        while i <= n-2:
            A.append( _ppcm( L[i] , L[i+1] ) )
            i += 2
        if n % 2 != 0:
            A.append( L[n-1] )
    
        return ppcm( A ) 


def _pgcd(a,b):
    """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b"""
    while b!=0:
        a,b=b,a%b
    return a

def pgcd(L):
    """Calcul du 'Plus Grand Commun Diviseur' de n valeurs entières (Euclide)"""
    p = _pgcd(L[0], L[1])
    for x in L[2:]:
        p = _pgcd(p, x)
    return p