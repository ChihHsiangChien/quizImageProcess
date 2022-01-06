import pandas as pd
import pygame
import os

df = pd.read_csv('data.csv')

pygame.init()

#### Create a canvas on which to display everything ####
window = (1300,750)
screen = pygame.display.set_mode(window)
pygame.display.set_caption( '評分程式')         


#### Create a canvas on which to display everything ####

#### Create a surface with the same size as the window ####
background = pygame.Surface(window)

#img = pygame.image.load( r'C:\Users\user\Documents\GitHub\quizImageProcess\answerImage\0\1090102周煜翔_0.png') 
#screen.blit(img,(0,0))

#取得目錄內所有圖片檔
imgPath = r'C:\Users\user\Documents\GitHub\quizImageProcess\answerImage_other\4'
imgList =[]
for path, subdirs, files in os.walk(imgPath):
    for name in files:
        #print(os.path.join(path, name))
        imgList.append( os.path.join(path, name) )
i = 0

def getData(i):
    path = imgList[i]
    firstpos=path.rfind("\\")
    lastpos=path.rfind("_")
    lastpos2=path.rfind(".")

    #print(path)
    #print(path[firstpos+1:lastpos])
    idName = path[firstpos+1:lastpos]
    id = idName[:7]
    questionNum = int(path[lastpos+1:lastpos2])
    return idName, id , questionNum



def loadImg(i):
    img = pygame.image.load( imgList[i])
    global done, press_1, press_2, press_3, press_4
    idName, id , questionNum = getData(i)

    filter1 = df['id'].str.contains(id)
    if int(df.loc[filter1,str(questionNum*5 + 0 )]) == 0:
        press_1 = False
    else:
        press_1 = True

    if int(df.loc[filter1,str(questionNum*5 + 1 )])== 0:
        press_2 = False
    else:
        press_2 = True

    if int(df.loc[filter1,str(questionNum*5 + 2 )] )== 0:
        press_3 = False
    else:
        press_3 = True

    if int(df.loc[filter1,str(questionNum*5 + 3 )] )== 0:
        press_4 = False
    else:
        press_4 = True




    return img



def updateDf(i, column = -1,value = -1):
    idName, id , questionNum = getData(i)

    filter1 = df['id'].str.contains(id)

    if column != -1:
        df.loc[filter1,str(questionNum*5 + (column-1))]  = value


def getSum(i):
    idName, id , questionNum = getData(i)
    filter1 = df['id'].str.contains(id)
    scores = 0 
    for k in range(4):
        scores = scores + df.loc[filter1,str(questionNum*5 + k) ]
    return int(scores)



img = loadImg(i)
updateDf(i)
screen.blit(img,(0,0))



pygame.display.flip()

done = False

offset = 4
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            df.to_csv('data.csv', index = False)
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if press_1 == False:
                    pygame.draw.rect(img,(255,0,0),(850+offset,200+offset,30-offset*2, 30-offset*2)) 
                    press_1 = True
                    updateDf(i,1,1)
                else:
                    pygame.draw.rect(img,(255,255,255),(850+offset,200+offset,30-offset*2, 30-offset*2)) 
                    press_1 = False
                    updateDf(i,1,0)

            if event.key == pygame.K_2:
                if press_2 == False:
                    pygame.draw.rect(img,(255,0,0),(850+offset,250+offset,30-offset*2, 30-offset*2))
                    press_2 = True
                    updateDf(i,2,1)
                else:
                    pygame.draw.rect(img,(255,255,255),(850+offset,250+offset,30-offset*2, 30-offset*2))
                    press_2 = False
                    updateDf(i,2,0)
    
            if event.key == pygame.K_3:
                if press_3 == False:
                    pygame.draw.rect(img,(255,0,0),(850+offset,300+offset,30-offset*2, 30-offset*2))
                    press_3 = True
                    updateDf(i,3,1)

                else:
                    pygame.draw.rect(img,(255,255,255),(850+offset,300+offset,30-offset*2, 30-offset*2))
                    press_3 = False
                    updateDf(i,3,0)


            if event.key == pygame.K_4:
                if press_4 == False:
                    pygame.draw.rect(img,(255,0,0),(850+offset,350+offset,30-offset*2, 30-offset*2))
                    press_4 = True
                    updateDf(i,4,1)

                else:
                    pygame.draw.rect(img,(255,255,255),(850+offset,350+offset,30-offset*2, 30-offset*2))
                    press_4 = False
                    updateDf(i,4,0)

            if event.key == pygame.K_5:
                pygame.image.save(img, imgList[i] )

            if event.key == pygame.K_PAGEUP or event.key == pygame.K_UP:
                pygame.image.save(img, imgList[i] )
                i -= 1
                if i <= 0 : i = len(imgList) -1
                img = loadImg(i)
                updateDf(i)
            if event.key == pygame.K_PAGEDOWN or event.key == pygame.K_DOWN:
                pygame.image.save(img, imgList[i] )
                i += 1
                if i >= len(imgList): i = 0
                img = loadImg(i)
                updateDf(i)

            if event.key == pygame.K_HOME:
                i = 0
                img = loadImg(i)
                updateDf(i)

            if event.key == pygame.K_END:
                i = len(imgList) -1
                img = loadImg(i)
                updateDf(i)


    score_sum = getSum(i)
    
    if score_sum == 0:
        pygame.draw.rect(img,(255,0,0),(850+offset,470+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,520+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,570+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,620+offset,30-offset*2, 30-offset*2))        
        updateDf(i,5,0)        
    elif score_sum <= 2 and score_sum >0:
        pygame.draw.rect(img,(255,255,255),(850+offset,470+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,0,0),(850+offset,520+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,570+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,620+offset,30-offset*2, 30-offset*2))        
        updateDf(i,5,3) 
    elif score_sum <4 and score_sum > 2:
        pygame.draw.rect(img,(255,255,255),(850+offset,470+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,520+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,0,0),(850+offset,570+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,620+offset,30-offset*2, 30-offset*2))        
        updateDf(i,5,6)         
    elif score_sum == 4:
        pygame.draw.rect(img,(255,255,255),(850+offset,470+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,520+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,255,255),(850+offset,570+offset,30-offset*2, 30-offset*2))
        pygame.draw.rect(img,(255,0,0),(850+offset,620+offset,30-offset*2, 30-offset*2))        
        updateDf(i,5,10) 


    screen.blit(img,(0,0))
    pygame.display.update()
pygame.quit()