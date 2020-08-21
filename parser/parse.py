import MeCab
import CaboCha
from collections import namedtuple

class JpParser:
  """
  return parsed data with Mecab
  """
  POS_DIC = {
    'BOS/EOS': 'EOS', # end of sentense
    '形容詞' : 'ADJ',
    '副詞'   : 'ADV',
    '名詞'   : 'NOUN',
    '動詞'   : 'VERB',
    '助動詞' : 'AUX',
    '助詞'   : 'PART',
    '連体詞' : 'ADJ', # Japanese-specific POS
    '感動詞' : 'INTJ',
    '接続詞' : 'CONJ',
    '*'      : 'X',
  }

  def __init__(self, * ,sys_dic_path=''):
    opt_m = "-Ochasen"
    opt_c = '-f4'
    if sys_dic_path:
      opt_m += ' -d {0}'.format(sys_dic_path)
      opt_c += ' -d {0}'.format(sys_dic_path)
    tagger = MeCab.Tagger(opt_m)
    tagger.parse('') # for UnicodeDecodeError
    self._tagger = tagger
    self._parser = CaboCha.Parser(opt_c)

  def get_sentences(self, text):
    """ 
    input: text have many sentences
    output: ary of sentences ['sent1', 'sent2', ...]
    """
    EOS_DIC = ['。', '．', '！','？','!?', '!', '?' ]
    sentences = list()
    sent = ''
    for token in self.tokenize(text):
      # print(token.pos_jp, token.pos, token.surface, sent)
      # TODO: this is simple way. ex)「今日は雨ね。」と母がいった
      sent += token.surface
      if token.surface in EOS_DIC and sent != '':
        sentences.append(sent)
        sent = ''
    return sentences


  def tokenize(self, sent):
    node = self._tagger.parseToNode( sent )
    tokens = list()
    idx = 0
    while node:
      feature = node.feature.split(',')
      token = namedtuple('Token', 'idx, surface, pos, pos_detail1, pos_detail2, pos_detail3,\
                          infl_type, infl_form, base_form, reading, phonetic')
      token.idx         = idx
      token.surface     = node.surface  # 表層形
      token.pos_jp      = feature[0]    # 品詞
      token.pos_detail1 = feature[1]    # 品詞細分類1
      token.pos_detail2 = feature[2]    # 品詞細分類2
      token.pos_detail3 = feature[3]    # 品詞細分類3
      token.infl_type   = feature[4]    # 活用型
      token.infl_form   = feature[5]    # 活用形
      token.base_form   = feature[6]    # 原型
      token.pos         = self.POS_DIC.get( feature[0], 'X' )     # 品詞
      token.reading     = feature[7] if len(feature) > 7 else ''  # 読み
      token.phonetic    = feature[8] if len(feature) > 8 else ''  # 発音
      #
      tokens.append(token)
      idx += 1
      node = node.next
    return tokens

if __name__ == "__main__":
  jp = JpParser( sys_dic_path='/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
  # Japanese famous poem written by Soseki natusme.
  sentences = jp.get_sentences('我輩は猫である。名前はまだ無い。どこで生れたかとんと見当けんとうがつかぬ。何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。吾輩はここで始めて人間というものを見た。')
  for sent in sentences:
    # token --------------------------------------
    sent_data = jp.tokenize(sent)
    for s in sent_data:
      print(s.surface, s.base_form, s.pos)

