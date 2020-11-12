#2020年8月6日発表「Bit-Based Division Propertyの紹介とIntegral・高階差分特性探索への適用」における6bitのFeistel暗号におけるIntegral・高階差分特性探索のシミュレーション

#入力部の特性は　aacccc
#つまり、上位2ビットで取りうる値すべてが出現し、残り4ビットは固定値である平文集合を用いるIntegral特性
#高階差分に対応させると、2階差分

#このプログラムではビット演算を用いているのでこのサイトを参照してほしい(http://www9.plala.or.jp/sgwr-t/c/sec14.html)

#実行すると，さまざまな鍵においてのXOR総和が出てくる
#そのXOR総和を縦に見て，ずっと０が続いているようなビット位置はIntegral特性b（攻撃に使用可能）
#0，1が混在しているビット位置はIntegral特性u（攻撃に使用不可）
#ちなみに，ずっと１が続くビット位置も攻撃に使用可能である その特性はIntegral特性 b' とでもしておこう(実用的な暗号ではほぼ出ることはないけど...)

#このプログラムはブロック長が6bitで高々5階差分までなので書きやすいpythonで実装している。
#卒研で64bit暗号などにこの手法を適用するならC,C++で書いた方が早く結果出る。もしくはpythonで記述して「pypy」を使うと速くなる模様(未検証)

import random
def main():
    print("入力Integral特性：aacccc")
    ROUND = int( input("何段分のintegral特性を求めますか？　：") )
    ATEMPT = 10000 #段鍵、平文のランダム設定の回数

    #出力部のIntegral特性　0で初期化
    output_integral=0b000000 

    for a in range(ATEMPT):
        #平文をランダムに設定
        plain_text = random.randint(0b000000,0b111111)
        #段鍵をランダムに設定
        keys = []
        for r in range(ROUND):
            keys.append( random.randint(0b000,0b111) )
        
        #排他的論理和の総和　初期値は全０に設定
        xor_sum=0b000000
        
        #Integral特性 aacccc の計算
        for delta_p in range(2**2):
            cryptgram = Mini_Feistel(plain_text ^ (delta_p<<4) ,keys,ROUND)#iを左に1ビットシフトさせて平文に排他して入力 これで最下位1ビットを固定している
            #print( "0b"+format(cryptgram, '06b'))#暗号文を2進数で出力
            xor_sum ^= cryptgram#暗号文の値を排他的論理和で足しこむ
        
        print(format(xor_sum,"06b"))#6ビットデータxor_sumを2進数表示（0詰め）
    
    

#6bitFeistel暗号の暗号器
#plain_text:6bits平文、keys：6bits段鍵の配列、ROUND：暗号器の段数
def Mini_Feistel(plain_text,keys,ROUND):

    #s-box
    #input 0b000 0b001 0b010 0b011 0b100 0b101 0b110 0b111 
    s_box=[0b100,0b110,0b000,0b011,0b111,0b001,0b101,0b010]#s-box(ただの配列)

    #data_right, data_left:それぞれ暗号器の右側、左側のデータ
    data_right=plain_text&0b111#0b111は2進数111 つまり平文plain_textの右３ビットをマスクで抽出して右側のデータとしている
    data_left=(plain_text>>3)&0b111#pを右に3ビット切り捨てシフトしてから0b111でマスク　つまり平文plain_textの左3ビットを抽出し左側のデータとしている

    for r in range(ROUND):
        temp=data_left#temp：一時的に左データを保存する
        #「 ^ 」がビット演算では排他的論理和
        data_left=data_right ^ s_box[ data_left ^ keys[r] ] #各段の左側の出力
        data_right=temp#各段の右側の出力
    
    cryptgram = (data_left<<3)^data_right #cryptgram：暗号文　ビット演算で左右のデータを結合している
    return cryptgram



if __name__=="__main__":
    main()
