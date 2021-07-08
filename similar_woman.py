import cv2, numpy as np
import matplotlib.pylab as plt
import dlib
import sys
import boto3

#얼굴 검출기와 랜드마크 검출기 생성
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('C:/Users/User/Desktop/termproject/k_beauty/shape_predictor_68_face_landmarks.dat')

#얼굴 및 랜드마크를 검출해서 좌표를 변환하는 함수
def getPoints(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray)
    points = []
    for rect in rects:
        shape = predictor(gray, rect)
        for i in range(68):
            part = shape.part(i)
            points.append((part.x, part.y))
    return points

#랜드마크 좌표로 들로네 삼각형 반환
def getTriangles(img, points):
    w,h = img.shape[:2]
    subdiv = cv2.Subdiv2D((0, 0,w,h));
    subdiv.insert(points)
    triangleList = subdiv.getTriangleList();
    triangles = []
    for t in triangleList:
        pt = t.reshape(-1,2)
        if not (pt<0).sum() and not (pt[:, 0] > w).sum() \
            and not (pt[:, 1]>h).sum():
            indice = []
            for i in range(0,3):
                for j in range(0, len(points)):
                    if(abs(pt[i][0] - points[j][0]) < 1.0 \
                        and abs(pt[i][1] - points[j][1])<1.0):
                        indice.append(j)
            if len(indice) == 3:
                triangles.append(indice)
    return triangles

def warpTriangle(img1, img2, pts1, pts2):
    x1,y1,w1,h1 = cv2.boundingRect(np.float32([pts1]))
    x2,y2,w2,h2 = cv2.boundingRect(np.float32([pts2]))

    roi1 = img1[y1:y1+h1, x1:x1+w1]
    roi2 = img2[y2:y2+h2, x2:x2+w2]

    offset1 = np.zeros((3,2), dtype=np.float32)
    offset2 = np.zeros((3,2), dtype=np.float32)
    for i in range(3):
        offset1[i][0], offset1[i][1] = pts1[i][0]-x1, pts1[i][1]-y1
        offset2[i][0], offset2[i][1] = pts2[i][0]-x2, pts2[i][1]-y2

    mtrx = cv2.getAffineTransform(offset1, offset2)
    warped = cv2.warpAffine( roi1, mtrx, (w2, h2), None, \
        cv2.INTER_LINEAR, cv2.BORDER_REFLECT_101)

    mask = np.zeros((h2, w2), dtype = np.uint8)
    cv2.fillConvexPoly(mask, np.int32(offset2), (255))

    warped_masked = cv2.bitwise_and(warped, warped, mask=mask)
    roi2_masked = cv2.bitwise_and(roi2, roi2, mask=cv2.bitwise_not(mask))
    roi2_masked = roi2_masked + warped_masked
    img2[y2:y2+h2, x2:x2+w2] = roi2_masked

# img1은 사용자 얼굴을 받아온 것이라 가정
img1 = cv2.imread('./sample.jpg')
img2 = cv2.imread('../image/woman/risabae.jpg')
img3 = cv2.imread('../image/woman/baecab.jpg')
img4 = cv2.imread('../image/woman/anda.jpg')
img5 = cv2.imread('../image/woman/jaeyou.jpg')
img6 = cv2.imread('../image/woman/yullimulli.jpg')
img7 = cv2.imread('../image/woman/dattoa.jpg')
img8 = cv2.imread('../image/woman/inbora.jpg')
img9 = cv2.imread('../image/woman/haesawona.jpg')
img10 = cv2.imread('../image/woman/sunny.jpg')
img11 = cv2.imread('../image/woman/soyoon.jpg')
img12 = cv2.imread('../image/woman/urishop.jpg')
img13 = cv2.imread('../image/woman/pony.jpg')
img14 = cv2.imread('../image/woman/mincarong.jpg')
img15 = cv2.imread('../image/woman/ssinnim.jpg')
img16 = cv2.imread('../image/woman/yocookie.jpg')
img17 = cv2.imread('../image/woman/youtrue.jpg')
img18 = cv2.imread('../image/woman/mamachoi.jpg')


#ssh에 바로 사진을 옮겨 실행하기 위한 코드
#img1 = cv2.imread('./sample.jpg')
#img2 = cv2.imread('./risabae.jpg')
#img3 = cv2.imread('./baecab.jpg')
#img4 = cv2.imread('./anda.jpg')
#img5 = cv2.imread('./jaeyou.jpg')
#img6 = cv2.imread('./yullimulli.jpg')
#img7 = cv2.imread('./dattoa.jpg')
#img8 = cv2.imread('./inbora.jpg')
#img9 = cv2.imread('./haesawona.jpg')
#img10 = cv2.imread('./sunny.jpg')
#img11 = cv2.imread('./soyoon.jpg')
#img12 = cv2.imread('./urishop.jpg')
#img13 = cv2.imread('./pony.jpg')
#img14 = cv2.imread('./mincarong.jpg')
#img15 = cv2.imread('./ssinnim.jpg')
#img16 = cv2.imread('./yocookie.jpg')
#img17 = cv2.imread('./youtrue.jpg')
#img18 = cv2.imread('./mamachoi.jpg')


youtuber = ["", "risabae", "baecab", "anda", "jeyu", "yullimulli", "daddoa", "inbora", "haesawona", "sunny", "soyoon", "urishop", "pony", "mincarong", "ssinnim", "yo-cookie", "yootrue", "mamachoi"]
address = ["", "https://www.youtube.com/channel/UC9kmlDcqksaOnCkC_qzGacA", "https://www.youtube.com/user/alswn1686", "https://www.youtube.com/channel/UCn_fZLXut_Tj9-QihG_9l0g", "https://www.youtube.com/channel/UC8P33HyFhfqThDUGk0disqw", "https://www.youtube.com/channel/UCiULanlNBXuMkaP9OiZWgYQ", "https://www.youtube.com/user/daddoatv", "https://www.youtube.com/channel/UCUrCIBJ3ScRAOLgPElscZqA", "https://www.youtube.com/user/calarygirl", "https://www.youtube.com/channel/UCxM21Vv4bWq106MxIPvrGQw", "https://www.youtube.com/channel/UCc_vOO8-XNMT8KmIVTEbt5g", "https://www.youtube.com/channel/UCceUWPM7SkvOmJ3bs9ZYJCw", "https://www.youtube.com/channel/UCT-_4GqC-yLY1xtTHhwY0hA", "https://www.youtube.com/channel/UCJC3eND1vV_MR_UJB7-E9LQ", "https://www.youtube.com/user/Hines382", "https://www.youtube.com/channel/UCtCRr4rDWjpRi8LSWexmCKg", "https://www.youtube.com/user/yootruebeutyroom", "https://www.youtube.com/channel/UC5GuM4v07hDr07rZyVADTdA"]

imgs = [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, img11, img12, img13, img14, img15, img16, img17, img18]

hists = []
for i, img in enumerate(imgs) :
    plt.subplot(1,len(imgs),i+1)
    plt.title('img%d'% (i+1))
    plt.axis('off') 
    plt.imshow(img[:,:,::-1])
    #---① 각 이미지를 HSV로 변환
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #---② H,S 채널에 대한 히스토그램 계산
    hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0, 256])
    #---③ 0~1로 정규화
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
    hists.append(hist)

a =[]
query = hists[0]
methods = {'CORREL' :cv2.HISTCMP_CORREL}
for j, (name, flag) in enumerate(methods.items()):
    for i, (hist, img) in enumerate(zip(hists, imgs)):
        #---④ 각 메서드에 따라 img1과 각 이미지의 히스토그램 비교
        ret = cv2.compareHist(query, hist, flag)
        if flag == cv2.HISTCMP_INTERSECT: #교차 분석인 경우 
            ret = ret/np.sum(query)        #비교대상으로 나누어 1로 정규화
        a.append(ret)
    a[0] = 0.0
    similar = a.index(max(a))
    print("Beauty Youtuber: ", youtuber[similar])
    print("Highest Correl: ", round(max(a),2))
    print("Channel Address: ", address[similar])
    
    if __name__ == '__main__' :
        img_draw = imgs[similar].copy()
        #각 이미지에서 얼굴 랜드마크 좌표 구하기
        points1 = getPoints(img1)
        points2 = getPoints(imgs[similar])
        #랜드마크 좌표로 볼록 선체 구하기
        hullIndex = cv2.convexHull(np.array(points2), returnPoints = False)
        hull1 = [points1[int(idx)] for idx in hullIndex]
        hull2 = [points2[int(idx)] for idx in hullIndex]
        #볼록 선체 안 들로네 삼각형 좌표 구하기
        triangles = getTriangles(imgs[similar], hull2)
        #각 삼각형 좌표로 삼각형 어핀 변환
        for i in range(0, len(triangles)):
            t1 = [hull1[triangles[i][j]] for j in range(3)]
            t2 = [hull2[triangles[i][j]] for j in range(3)]
            warpTriangle(img1, img_draw, t1, t2)
        #블록 선체를 마스크로 써서 얼굴 합성
        mask = np.zeros(imgs[similar].shape, dtype = imgs[similar].dtype)
        cv2.fillConvexPoly(mask, np.int32(hull2), (255, 255, 255))
        r=cv2.boundingRect(np.float32([hull2]))
        center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))
        output = cv2.seamlessClone(np.uint8(img_draw), imgs[similar], mask, center, \
            cv2.NORMAL_CLONE)
        save_file = '../image/woman/swap_woman.jpg'
        cv2.imwrite(save_file, output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #버킷에 swap파일 전송
        s3 = boto3.client('s3',
            aws_access_key_id = "YOUR_ID",
            aws_secret_access_key = "YOUR_KEY")
        s3.upload_file(save_file, 'yourbucketname', 'swap.jpg')
    print()