import streamlit as st
st.title('동욱이 다이어트 2일차')
a=st.text_input('이름을 입력하세요!')
b=st.selectbox('좋아하는 음식을 선택하세요',['밍글스','정식닥','소나','산','이타닉가든'])
if st.button('인사말 생성'):
st.write('반갑습니다')
