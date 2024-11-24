#!/usr/bin/python
import random
import math

#数値生成
def num_generate(n):
    p = [] #nビットのリスト

    #各ビットにランダムな値を追加
    for j in range(n-1):
        p.append(random.randint(0, 1))
    p.append(1)

    #10進数に変換
    num = 0
    for j in range(n):
        num += p[j] * pow(2, j)

    return num

#素数判定（Miller-Rabinテスト）
def miller_rabin(p, S):
    if(p < 2): #pが0か1なら素数ではない
        return 1
    if(p == 2):
        return 0
    elif(p % 2 == 0): #pが2を除いた偶数なら素数ではない
        return 1
    v = (p - 1) // 2
    while v % 2 == 0:
        v //= 2
    u = int(math.log(((p - 1) / v), 2))
    for i in range(S):
        a = random.randint(2, p-1)
        if(pow(a, p-1, p) != 1): #素数でないと判定して終了
            return 1
        for j in range(1, u):
            if(pow(a, 2 * j * v, p) == 1
               and pow(a, pow(2, (j - 1)) * v, p) != 1
               and pow(a, pow(2, (j - 1)) * v, p) != p-1):
                return 1
           
    return 0

#ユークリッド互除法
def euclid(tmp1, tmp2):
    a = [] #数値配列
    quo = [0] #商の配列
    # 入力された数字を配列aに格納
    a.append(tmp1)
    a.append(tmp2)

    #ユークリッド互除法
    i = 0
    while(a[i+1] != 0):
        a.append(a[i]%a[i+1]) #配列aに剰余を格納
        quo.append(int(a[i]/a[i+1])) #配列quoに商を格納
        i += 1
    return a[i], quo, i

#拡張ユークリッド
def wide_euclid(quo, i):
    #逆元の配列
    alpha = []
    beta = []
    for j in range(i+1):
        if(j == 0): #j=0
            alpha.append(1)
            beta.append(0)
        elif(j == 1): #j=1
            alpha.append(0)
            beta.append(1)
        else: #j>=2における漸化式
            alpha.append(alpha[j-2]-quo[j-1]*alpha[j-1])
            beta.append(beta[j-2]-quo[j-1]*beta[j-1])
    return beta[j]

#main
prime = [] #素数リスト
count = 0 #素数の個数

#メッセージの入力
m = input("メッセージ(数値)を入力: ") #メッセージの入力
m = int(m)
print("・")
print("・")
print("・")

#素数の生成
while count < 2:
    n = 512 #ビット数
    S = n #最大繰り返し回数S
    p = num_generate(n)
    if(miller_rabin(p, S) == 0):
        prime.append(p)
        count += 1
    # print(prime, count)

p, q = prime[0], prime[1]

print(f"生成された素数: ① {p} ② {q}\n")

n = p*q #Nを計算

#gcd((p−1)(q−1), e) = 1 かつe < (p-1)(q-1)となる自然数eの生成
while True:
    e = random.randint(1, (p-1)*(q-1)-1)
    if(euclid((p-1)*(q-1), e)[0]==1):
        break

quo = euclid((p-1)*(q-1), e)[1]
i = euclid((p-1)*(q-1), e)[2]

#秘密鍵の生成
d = wide_euclid(quo, i)
if(d < 0):
    d += (p-1)*(q-1)
print(f"公開鍵: ① {n} ② {e}\n")
print(f"秘密鍵: {d}\n")

#暗号化
c = pow(m, e, n) #暗号文の計算
print(f"暗号文: {c}\n")

#複合化
m_alt = pow(c, d, n)
print(f"平文: {m_alt}")