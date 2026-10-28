import streamlit as st
st.title('동욱이 다이어트 2일차')
a=st.text_input('이름을 입력하세요!')
b=st.selectbox('좋아하는 음식을 선택하세요',['밍글스','정식닥','소나','산','이타닉가든'])
if st.button('인사말 생성'):
  st.write('반갑습니다')
  st.info(a+'님,안녕하세요!')
  st.warning(b+'를 좋아하시네요!')
  st.error(잘부탁드려요!')
  st.balloons()
  st.staes()
  st.fire()
