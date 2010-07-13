from sympy.physics.qbit import *
from sympy import symbols, Rational
from sympy.core.numbers import *
from sympy.functions.elementary import *
import random
x, y = symbols('xy')

epsilon = .000001

def test_represent_Hadamard_Z():
    circuit = HadamardGate(0)*Qbit(0, 0)
    answer = represent(circuit, ZBasisSet())
    # check that the answers are same to within an epsilon
    assert answer == Matrix([1/sqrt(2),1/sqrt(2), 0, 0])

def test_represent_XGate_Z():
    circuit = XGate(0)*Qbit(0,0)
    answer = represent(circuit, ZBasisSet())
    assert Matrix([0, 1, 0, 0]) == answer

def test_represent_YGate_Z():
    circuit = YGate(0)*Qbit(0,0)
    answer = represent(circuit, ZBasisSet())
    assert answer[0] == 0 and answer[1] == ImaginaryUnit() and answer[2] == 0 and answer[3] == 0

def test_represent_ZGate_Z():
    circuit = ZGate(0)*Qbit(0,0)
    answer = represent(circuit, ZBasisSet())
    assert Matrix([1, 0, 0, 0]) == answer

def test_represent_PhaseGate_Z():
    circuit = PhaseGate(0)*Qbit(0,1)
    answer = represent(circuit, ZBasisSet())
    assert Matrix([0, ImaginaryUnit(),0,0]) == answer 

def test_represent_TGate_Z():
    circuit = TGate(0)*Qbit(0,1)
    assert Matrix([0, exp(I*Pi()/4), 0, 0]) == represent(circuit)

def test_CompoundGates_Z():
    circuit = YGate(0)*ZGate(0)*XGate(0)*HadamardGate(0)*Qbit(0, 0)
    answer = represent(circuit)
    assert Matrix([.5*ImaginaryUnit()*sqrt(2),ImaginaryUnit()/sqrt(2), 0, 0]) == answer

def test_CNOTGate():
    circuit = CNOTGate(1,0)
    assert represent(circuit, HilbertSize = 2) == Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    circuit = circuit*Qbit(1,1,1)
    assert matrix_to_qbits(represent(circuit)) == apply_gates(circuit)

def test_ToffoliGate():
    circuit = ToffoliGate(2,1,0)
    assert represent(circuit, HilbertSize = 3) == Matrix([[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,1,0]])

    circuit = ToffoliGate(3,0,1)
    assert apply_gates(circuit*Qbit(1,0,0,1)) == matrix_to_qbits(represent(circuit*Qbit(1,0,0,1)))
    assert apply_gates(circuit*Qbit(0,0,0,0)) == matrix_to_qbits(represent(circuit*Qbit(0,0,0,0)))

def test_SwapGate():
    assert apply_gates(SwapGate(0,1)*Qbit(1,0)) == Qbit(0,1)
    assert Qbit(0,1,0) == apply_gates(SwapGate(1,0)*SwapGate(0,1)*Qbit(0,1,0))
    assert matrix_to_qbits(represent(SwapGate(0,1)*Qbit(1,0))) == Qbit(0,1)
    assert Qbit(0,1,0) == matrix_to_qbits(represent(SwapGate(1,0)*SwapGate(0,1)*Qbit(0,1,0)))

def test_ControlledZ_Gate():
    assert apply_gates(CZGate(0,1)*Qbit(1,1)) == -Qbit(1,1)
    assert matrix_to_qbits(represent(CZGate(0,1)*Qbit(1,1))) == -Qbit(1,1)

def test_CPhase_Gate():
    assert apply_gates(CPhaseGate(0,1)*Qbit(1,1)) == ImaginaryUnit()*Qbit(1,1)
    assert matrix_to_qbits(represent(CPhaseGate(0,1)*Qbit(1,1))) == ImaginaryUnit()*Qbit(1,1)

def test_gateSort():
    assert gatesort(HadamardGate(0)*XGate(1)*HadamardGate(0)**2*CNOTGate(0,1)*XGate(1)*XGate(0)) == HadamardGate(0)**3*XGate(1)*CNOTGate(0,1)*XGate(0)*XGate(1)

def test_gatesimp():
     assert gatesimp(HadamardGate(0)*XGate(1)*HadamardGate(0)**2*CNOTGate(0,1)*XGate(1)**3*XGate(0)*ZGate(3)**2*PhaseGate(4)**3) == HadamardGate(0)*XGate(1)*CNOTGate(0,1)*XGate(0)*XGate(1)*ZGate(4)*PhaseGate(4)

def test_gate_qbit_strings():
    assert sstr(Qbit(0,1)) == "|01>"
    assert sstr(HadamardGate(3)) == "H(3)"
    assert sstr(XGate(2)) == "X(2)"
    assert sstr(ZGate(6)) == "Z(6)"
    assert sstr(YGate(6)) == "Y(6)"
    assert sstr(CNOTGate(1,0)) == "CNOTGate(1, 0)"

def test_ArbMat4_apply():
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p = symbols('abcdefghijklmnop')
    class Arb(Gate):
        @property
        def matrix(self):
            return Matrix([[a,b,c,d],[e,f,g,h],[i,j,k,l],[m,n,o,p]])

    assert apply_gates(Arb(1,0)*Qbit(0,0,1,0,1)) == b*Qbit(0,0,1,0,0) + f*Qbit(0,0,1,0,1) + j*Qbit(0,0,1,1,0) + n*Qbit(0,0,1,1,1)
    assert apply_gates(Arb(2,4)*Qbit(0,0,1,0,1)) == c*Qbit(0,0,0,0,1) + g*Qbit(1,0,0,0,1) + k*Qbit(0,0,1,0,1) + o*Qbit(1,0,1,0,1)
    assert apply_gates(Arb(3,0)*Qbit(1,1,1,1,1)) == d*Qbit(1,0,1,1,0) + h*Qbit(1,0,1,1,1) + l*Qbit(1,1,1,1,0) + p*Qbit(1,1,1,1,1)
    assert apply_gates(Arb(6,9)*Qbit(0,1,1,0,1,1,0,1,0,1)) == a*Qbit(0,1,1,0,1,1,0,1,0,1) + e*Qbit(1,1,1,0,1,1,0,1,0,1) + i*Qbit(0,1,1,1,1,1,0,1,0,1) + m*Qbit(1,1,1,1,1,1,0,1,0,1)

def test_ArbMat8_apply():
    a,b,c,d,e,f,g,h = symbols('abcdefgh')
    class Arb(Gate):
        @property
        def matrix(self):
            symlist = [a,b,c,d,e,f,g,h]
            lout = []
            for i in range(8):
                lin = []
                for j in range(8):
                    lin.append(symlist[i]**j)
                lout.append(lin)
            return Matrix(lout)    

    assert apply_gates(Arb(2,1,0)*Qbit(0,1,1,0,1)) == a**5*Qbit(0,1,0,0,0) + b**5*Qbit(0,1,0,0,1) + c**5*Qbit(0,1,0,1,0) + d**5*Qbit(0,1,0,1,1) + e**5*Qbit(0,1,1,0,0) + f**5*Qbit(0,1,1,0,1) + g**5*Qbit(0,1,1,1,0) + h**5*Qbit(0,1,1,1,1)
    assert apply_gates(Arb(0,4,3)*Qbit(1,1,0,1,0)) == a**3*Qbit(0,0,0,1,0) + b**3*Qbit(0,1,0,1,0) + c**3*Qbit(1,0,0,1,0) + d**3*Qbit(1,1,0,1,0) + e**3*Qbit(0,0,0,1,1) + f**3*Qbit(0,1,0,1,1) + g**3*Qbit(1,0,0,1,1) + h**3*Qbit(1,1,0,1,1)
    assert apply_gates(Arb(4,1,3)*Qbit(0,1,0,0,1,0)) == a**6*Qbit(0,0,0,0,0,0) + b**6*Qbit(0,0,1,0,0,0) + c**6*Qbit(0,0,0,0,1,0) + d**6*Qbit(0,0,1,0,1,0) + e**6*Qbit(0,1,0,0,0,0) + f**6*Qbit(0,1,1,0,0,0) + g**6*Qbit(0,1,0,0,1,0) + h**6*Qbit(0,1,1,0,1,0)
    assert apply_gates(Arb(3,1,4)*Qbit(0,1,0,1,0,0,1,0,1)) == Qbit(0,1,0,1,0,0,1,0,1) + Qbit(0,1,0,1,1,0,1,0,1) + Qbit(0,1,0,1,0,0,1,1,1) + Qbit(0,1,0,1,1,0,1,1,1) + Qbit(0,1,0,1,0,1,1,0,1) + Qbit(0,1,0,1,1,1,1,0,1) + Qbit(0,1,0,1,0,1,1,1,1) + Qbit(0,1,0,1,1,1,1,1,1)
    assert apply_gates(Arb(8,10,9)*Qbit(1,1,1,0,1,0,1,0,1,0,1)) == a**7*Qbit(0,0,0,0,1,0,1,0,1,0,1) + b**7*Qbit(0,1,0,0,1,0,1,0,1,0,1) + c**7*Qbit(1,0,0,0,1,0,1,0,1,0,1) + d**7*Qbit(1,1,0,0,1,0,1,0,1,0,1) + e**7*Qbit(0,0,1,0,1,0,1,0,1,0,1) + f**7*Qbit(0,1,1,0,1,0,1,0,1,0,1) + g**7*Qbit(1,0,1,0,1,0,1,0,1,0,1) + h**7*Qbit(1,1,1,0,1,0,1,0,1,0,1)
    assert apply_gates(Arb(9,2,3)*Qbit(0,1,1,1,1,1,1,0,1,1)) == a*Qbit(0,1,1,1,1,1,0,0,1,1) + b*Qbit(0,1,1,1,1,1,1,0,1,1) + c*Qbit(0,1,1,1,1,1,0,1,1,1) + d*Qbit(0,1,1,1,1,1,1,1,1,1) + e*Qbit(1,1,1,1,1,1,0,0,1,1) + f*Qbit(1,1,1,1,1,1,1,0,1,1) + g*Qbit(1,1,1,1,1,1,0,1,1,1) + h*Qbit(1,1,1,1,1,1,1,1,1,1)
    assert apply_gates(Arb(2,1,0)*Qbit(0,1,0)) == a**2*Qbit(0,0,0) + b**2*Qbit(0,0,1) + c**2*Qbit(0,1,0) + d**2*Qbit(0,1,1) + e**2*Qbit(1,0,0) + f**2*Qbit(1,0,1) + g**2*Qbit(1,1,0) + h**2*Qbit(1,1,1)
    
def test_ArbMat4_Equality():

    class Arb(Gate):
        @property
        def matrix(self):
            a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p = symbols('abcdefghijklmnop')
            return Matrix([[a,b,c,d],[e,f,g,h],[i,j,k,l],[m,n,o,p]])
        
    for i in range(4):
        for j in range(4):
            if j != i:
                assert apply_gates(Arb(i,j)*(Qbit(1,0,1,1,0))) == matrix_to_qbits(represent(Arb(i,j)*(Qbit(1,0,1,1,0)), format = 'numpy'))   

def test_Arb8_Matrix_Equality():
    class Arb(Gate):
        @property
        def matrix(self):
            a,b,c,d,e,f,g,h = symbols('abcdefgh')
            symlist = [a,b,c,d,e,f,g,h]
            lout = []
            for i in range(8):
                lin = []
                for j in range(8):
                    lin.append(symlist[i]**j)
                lout.append(lin)
            return Matrix(lout)

    for i in range(4):
        for j in range(4):
            for k in range(4):
                if j != i and k != i and k != j:
                    assert apply_gates(Arb(i,j,k)*(Qbit(0,1,1,1,0))) == matrix_to_qbits(represent(Arb(i,j,k)*(Qbit(0,1,1,1,0)), format = 'numpy'))     

def test_superposition_of_states():
    assert apply_gates(CNOTGate(0,1)*HadamardGate(0)*(1/sqrt(2)*Qbit(0,1) + 1/sqrt(2)*Qbit(1,0))) == (Qbit(0,1)/2 + Qbit(0,0)/2 - Qbit(1,1)/2 + Qbit(1,0)/2)
    assert matrix_to_qbits(represent(CNOTGate(0,1)*HadamardGate(0)*(1/sqrt(2)*Qbit(0,1) + 1/sqrt(2)*Qbit(1,0)))) == (Qbit(0,1)/2 + Qbit(0,0)/2 - Qbit(1,1)/2 + Qbit(1,0)/2)
    
    
def test_tensor_product():
    try:
        import numpy as np
    except ImportError:
        return
    l1 = zeros(4)
    for i in range(16):
        l1[i] = 2**i
    l2 = zeros(4)
    for i in range(16):
        l2[i] = i
    l3 = zeros(2)
    for i in range(4):
        l3[i] = i
    vec = Matrix([1,2,3])

    #test for Matrix known 4x4 matricies
    numpyl1 = np.matrix(l1.tolist())
    numpyl2 = np.matrix(l2.tolist())
    numpy_product = np.kron(numpyl1,numpyl2)
    args = [l1, l2]
    sympy_product = TensorProduct(*args)
    assert numpy_product.tolist() == sympy_product.tolist()
    numpy_product = np.kron(numpyl2,numpyl1)
    args = [l2, l1]
    sympy_product = TensorProduct(*args)    
    assert numpy_product.tolist() == sympy_product.tolist()

    #test for other known matrix of different dimensions
    numpyl2 = np.matrix(l3.tolist())
    numpy_product = np.kron(numpyl1,numpyl2)
    args = [l1, l3]
    sympy_product = TensorProduct(*args)
    assert numpy_product.tolist() == sympy_product.tolist()
    numpy_product = np.kron(numpyl2,numpyl1)
    args = [l3, l1]
    sympy_product = TensorProduct(*args)    
    assert numpy_product.tolist() == sympy_product.tolist()    

    #test for non square matrix
    numpyl2 = np.matrix(vec.tolist())
    numpy_product = np.kron(numpyl1,numpyl2)
    args = [l1, vec]
    sympy_product = TensorProduct(*args)
    assert numpy_product.tolist() == sympy_product.tolist()
    numpy_product = np.kron(numpyl2,numpyl1)
    args = [vec, l1]
    sympy_product = TensorProduct(*args)    
    assert numpy_product.tolist() == sympy_product.tolist()   

    #test for random matrix with random values that are floats    
    random_matrix1 = np.random.rand(np.random.rand()*5+1,np.random.rand()*5+1)
    random_matrix2 = np.random.rand(np.random.rand()*5+1,np.random.rand()*5+1)
    numpy_product = np.kron(random_matrix1,random_matrix2)
    args = [Matrix(random_matrix1.tolist()),Matrix(random_matrix2.tolist())]
    sympy_product = TensorProduct(*args)
    assert not (sympy_product - Matrix(numpy_product.tolist())).tolist() > (ones((sympy_product.rows,sympy_product.cols))*epsilon).tolist()

    #test for three matrix kronecker
    sympy_product = TensorProduct(l1,vec,l2)
    npl1 = np.matrix(l1.tolist())
    npl2 = np.matrix(l2.tolist())
    npvec = np.matrix(vec.tolist())

    numpy_product = np.kron(l1,np.kron(vec,l2)) 
    assert numpy_product.tolist() == sympy_product.tolist()

#test apply methods
def test_apply_represent_equality():
    gates = [HadamardGate(int(5*random.random())), XGate(int(5*random.random())), ZGate(int(5*random.random())), YGate(int(5*random.random())), ZGate(int(5*random.random())), PhaseGate(int(5*random.random()))]
    
    circuit = Qbit(int(random.random()*2),int(random.random()*2),int(random.random()*2),int(random.random()*2),int(random.random()*2),int(random.random()*2))
    circuit = HadamardGate(2)*HadamardGate(4)*HadamardGate(5)*HadamardGate(1)*HadamardGate(0)*HadamardGate(3)*circuit
    for i in range(int(random.random()*6)):
        circuit = gates[int(random.random()*6)]*circuit


    mat = represent(circuit)
    states = apply_gates(circuit)
    state_rep = matrix_to_qbits(mat)
    states = states.expand()
    state_rep = state_rep.expand()
    assert state_rep == states

