import tensorflow as tf
# hello=tf.constant("hello")
# print(hello) # 출력결과 : 텐서 정보 Tensor("Const:0", shape=(), dtype=string)
#
# #정보를 나타내고 싶으면 그래프를 실행해야함
# # 색션 만들기
# sess= tf.Session()
# #print(sess) # 세션 정보 확인
#
# print(sess.run(hello)) # 그래프 실행
# print(str(sess.run(hello),encoding='utf-8'))
#
#
# a= tf.constant(5,dtype=tf.float32) # 상수를 준거니까 변하지 않는 값. 이렇게 생각하면됨.
# b= tf.constant(10,dtype=tf.float32) # d라는 연산 e
# c= tf.constant(2,dtype=tf.float32) #
# d= a*b+c # a에 b를 곱한 후 c로 더한 연산을 d라는 노드로 정의한다.
# #d에 대입한다가 아님 완전 다른 의미로 d라는 노드가 생성이 된것.
# # 실행이 될때 a안에 5가 들어가지 않는다는 차이가있음
#
#
# ###########  그래프 정의 부분
#
# sess= tf.Session()
# res=sess.run(d) # d노드를 실행한 결과를 res에 저장해라
# #텐서플로우는 위에서부터 오는것이 아니라 여기서 색션을 실행하는 시점 그때서야 비로소 노드가 생성됨.
# print(res)
#
# a=tf.constant(3)
# print(a)
# # 세션 실행 1
# # sess=tf.Session()
# # print(sess.run(a))
# #sess.close() 세션 종료 -> 메모리 자원 반환
#
#
# #세션 실행 2
# #with의 장점 :
# # 위드 구문을 썼을 경우 close를 신경안쓸수 있어서 편하다.
# with tf.Session() as sess:
#     # sess라는 이름으로 세션 객체를 만들어라
#     # with구문의 들여쓰기 레벨이 세션 객체가 유효한 범위를 나타냄.
#     print(sess.run(a))
#     print(a.eval()) # 함수 호출처럼 별도에 만들어진 값을 가지고오는 가능 그래서 with에서 갖고옴
#     # 들여쓰기를 제대로 안한 곳으로 가면 세션 종료가 됨.
#     # 현재 위치에서 세션이 종료
# # print(sess.run(a)) 오류

# a=tf.constant(5)
# b=tf.constant(3)
# c= tf.multiply(a,b)# c=a*b
# d=tf.add(a,b)#d=a+b
# e=tf.add(c,d)#e=c+d
# sess=tf.Session()
# print(sess.run(e))

# inputdata=[1,2,3]
# x=tf.placeholder(dtype=tf.float32) # 실행시점에 데이터가 전달
# #실행하는 시점에 외부로 부터 값을 홀딩하고 있다가 값을 전달해줌.
# y= x*2
# sess=tf.Session()
# res=sess.run(y,feed_dict={x:inputdata})
# print(res)
#
# a= tf.placeholder(dtype=tf.float32)
# b= tf.placeholder("float")
# y= tf.multiply(a,b)
# z= tf.add(y,y)
#
# ####그래프 정의 ######
# sess = tf.Session()
# ## 그래프 실행 ##
# #print(sess.run(y,feed_dict={a:3,b:2}))
#
# #a 노드를 실행 , 결과가 10이 출력 되도록 구문 적기
# # print(sess.run(a,feed_dict={a:10}))
# #z노드 실행, y는 a(3)*b(2) 값 => 12 출력
# print(sess.run(z,feed_dict={a:3,b:2}))

#
# #################################3
#
# x=tf.constant(15)
# y=tf.Variable(x+5) # 변수는 초기화를 해줘야지 실행됨.
#
#
# ###변수초기화$$
# sess=tf.Session()
# init=tf.global_variables_initializer() # 변수 초기화
# sess.run(init) #변수실행. 반드시 세줄은 먼저 실행해주어야힘.
# ####
# print(sess.run(y))

# input=[1,2,3,4,5]
# x=tf.placeholder(dtype=tf.float32)
# w=tf.Variable(2,dtype=tf.float32)
# y=tf.multiply(w,x)
#
# sess= tf.Session()
# init = tf.global_variables_initializer()
# sess.run(init)
# print(sess.run(y,feed_dict={x:input})) #[2. 4. 6. 8. 10.]

# x=tf.linspace(-1.0,1.0,10)
# sess= tf.Session()
# print(sess.run(x))
# sess.close()
#
# a=tf.placeholder("float")
# b=tf.placeholder("float")
# y=tf.multiply(a,b)
# z= tf.add(y,y)
# with tf.Session() as sess :
#     print(sess.run(z,feed_dict={a:4,b:4}))


# x= tf.constant([[1.0, 2.0, 3.0]]) # 1행 3열
# w= tf.constant([[2.0],[ 2.0], [2.0]]) # 3행 1열
# y=tf.matmul(w,x) # 함수이름 달라짐
# # 행렬에 곱셈이기 때문에 y=tf.matmul(w,x) 와 y=tf.matmul(x,w) 값이 달라짐
# sess=tf.Session()
# res=sess.run(y)
# print(res)


# x= tf.Variable([[1.0, 2.0, 3.0]]) # 1행 3열
# w= tf.constant([[2.0],[ 2.0], [2.0]]) # 3행 1열
# y=tf.matmul(x,w) # multply랑 완전 다름
# sess=tf.Session()
# init=tf.global_variables_initializer()
# sess.run(init)
# res=sess.run(y)
# print(res)

# #             1회   2회  3 회
# input_data= [[1.0, 2.0, 3.0],[1.0, 2.0, 3.0],[2.0, 3.0, 4.0]] # 3행 3열
# x= tf.placeholder(dtype=tf.float32, shape=[None,3]) # 행 :?, 열:3
# # shape=[None] 텐서플로우에서 None은 값이 정해져 있지 않는 상황을 말함.
# w= tf.Variable([[2.0],[ 2.0], [2.0]])
# # W를 찾아내는게 아주 중요함,. 변화할 수 있으므로 variable , W의 초기값은 2
# y=tf.matmul(x,w) # multply랑 완전 다름
# sess=tf.Session()
# init=tf.global_variables_initializer()
# sess.run(init)
# res=sess.run(y,feed_dict={x:input_data})
# print(res)

# 8월 모의고사 9월 모의고사 10월 모의고사 수능점수 / 100 200 100 150  열의 개수는 4개 /5명에 대한 점수는 5행 4열
#이런경우 열은 거의 고정으로 있으나 데이타 인스턴스의 갯수 즉 사람의 갯수가 달라짐. 보통 데이터가 계속 늘어남
# 데이터는 계속 추가가 됨. 행의 계수가 고정이 안되어있음



input1=tf.constant([3.0])
input2=tf.constant([2.0])
input3=tf.constant([5.0])
inter=tf.add(input2,input3)
mul=tf.multiply(input1,inter)
with tf.Session() as sess:
    # res = sess.run([mul,inter])
    res1,res2 = sess.run([mul,inter])
    mulres = sess.run(mul)
    mulinter = sess.run(inter)
# print(res[0]) # res만 했을경우 array 로 나오게 됨.
print(res1)
print(res2)
print(mulres)
print(mulinter)
print(mulinter)