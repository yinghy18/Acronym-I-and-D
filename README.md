# Acronym-I-and-D

rule based 算法复现与实验：
判断short form的rules如下：
1.  需要出现在括号内（此条可根据不同的数据集变换）
2.  字符长度在2-10之间
3.  大写加数字占字符总长不少于三分之一，数字不超过三分之二，必须有大写字母
4.  不能以标点结尾

提取long form candidate的算法如下：
找到short form出现的位置，从那个地方往前，在同一个句子（采用了nltk分句）里并且长度不大于min(a+5,2a)的词组。

判断是否为long form：
对给定的sf-lf candidate pair，从后向前匹配short form中的每一个字符（不包括标点）。即需要满足：
1. short form的每一个字符（不包括标点）都在long form里出现，做小写化
2. short form的第一个字符应当和long form第一个单词的第一个字符相同
3. 如遇到short form结尾是数字或疑似罗马数字，需要考虑数字和罗马数字直接的对应关系再进行匹配。

每一个sf有可能在上述情况下对应多个lf，一并采用。
有的sf找不到对应的lf，此为缩写的特殊情况，即有些缩写的原文难以用这些rules表示出来。


结果：
short form 识别：平均precision 0.732715461982739 其中766/1201个precision=1  平均recall 0.7357628563498672 其中776/1201个recall=1  平均f1 0.720902973779252  其中662/1201个f1=1

sf-lf pair 识别：平均precision 0.7433414074130139 其中769/1201个precision=1  平均recall 0.724846358193569 其中739/1201个recall=1  平均f1 0.718665681670194  其中638/1201个f1=1

bad case展示：
short form未能识别的例子：
V (variant)
wt (wild-type)
mAbs (Monoclonal antibodies)
UDP-glucose (Uridine 5'-diphosphoglucose)
alpha1A(+NP) (alpha1A channel with NP)
so (sine oculis)
gamma IP-10 (interferon gamma (IFN-gamma)-inducible protein 10)

少量因原文分词导致的问题

识别出short之后，未能识别到long form的例子：
CaMKII ———— Ca2+/calmodulin-dependent protein kinase
MPG protein ———— 3-Methyladenine-DNA glycosylase
TMPRSS3 ———— transmembrane serine protease


错误识别：
IGF-I ———— insulin and the insulin-like growth factor-1  （正确的从the之后开始）
ER ———— extended endoplasmic reticulum （正确的是后两个词）
（原因基本类似，因为允许的最大长度中，有开头一样的别的词）

错误sf识别：
CZ  原句：specially in the repeats of charged amino acid-rich region with leucine-zipper like sequences (CZ region/HR1)
E3, E1, E2  原句：We now report that Mdm2 is a ubiquitin protein ligase (E3)
Praja1  原句：Replacement of the Mdm2 RING with that of another protein (Praja1)
（类似的错误识别不再写，原因均为括号内为举例、解释说明而产生的的short form，而不是指示了前面的某个phrase，也就是不会找到对应的lf。letter match算法确实不输出sf-lf pair了）



