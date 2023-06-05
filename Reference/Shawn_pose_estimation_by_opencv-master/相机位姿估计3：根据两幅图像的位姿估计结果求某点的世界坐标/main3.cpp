#include "stdafx.h"
#include <opencv2\opencv.hpp>

#include <include/PNPSolver.h>
#include "..\include\PNPSolver.h"
#include "..\include\GetDistanceOf2linesIn3D.h"
using namespace std;

const int F = 350;//�����ͷ����


//�ú������ڼ���ĳ�����������
//�������
//pointInImage1���������ͼ1�еĶ�ά����
//p4psolver1��ͼ1�����PNPSolver��
//pointInImage2���������ͼ2�еĶ�ά����
//p4psolver2��ͼ2�����PNPSolver��
//����
//���������������ϵ������
cv::Point3f GetPointInWorld(cv::Point2f pointInImage1, PNPSolver& p4psolver1, cv::Point2f pointInImage2, PNPSolver& p4psolver2)
{

	//��PͶ�䵽�������ϵ���پ�������ת�������OcP�����ջ��ͼ1�У�ֱ��OcP�ϵ����������꣬ȷ����ֱ�ߵķ���
	cv::Point3f point2find1_CF = p4psolver1.ImageFrame2CameraFrame(pointInImage1, F);//�����P��ͼһ״̬�µ��������ϵ����
	double Oc1P_x1 = point2find1_CF.x;
	double Oc1P_y1 = point2find1_CF.y;
	double Oc1P_z1 = point2find1_CF.z;
	//�������η�����ת���õ���������ϵ������OcP��ֵ
	PNPSolver::CodeRotateByZ(Oc1P_x1, Oc1P_y1, p4psolver1.Theta_W2C.z, Oc1P_x1, Oc1P_y1);
	PNPSolver::CodeRotateByY(Oc1P_x1, Oc1P_z1, p4psolver1.Theta_W2C.y, Oc1P_x1, Oc1P_z1);
	PNPSolver::CodeRotateByX(Oc1P_y1, Oc1P_z1, p4psolver1.Theta_W2C.x, Oc1P_y1, Oc1P_z1);
	//����ȷ��һ��ֱ��
	cv::Point3f a1(p4psolver1.Position_OcInW.x, p4psolver1.Position_OcInW.y, p4psolver1.Position_OcInW.z);
	cv::Point3f a2(p4psolver1.Position_OcInW.x + Oc1P_x1, p4psolver1.Position_OcInW.y + Oc1P_y1, p4psolver1.Position_OcInW.z + Oc1P_z1);











	//��PͶ�䵽�������ϵ���پ�������ת�������Oc1P�����ջ��ͼ2�У�ֱ��Oc2P�ϵ����������꣬ȷ����ֱ�ߵķ���
	cv::Point3f point2find2_CF = p4psolver2.ImageFrame2CameraFrame(pointInImage2, F);//�����P��ͼ��״̬�µ��������ϵ����
	double Oc2P_x2 = point2find2_CF.x;
	double Oc2P_y2 = point2find2_CF.y;
	double Oc2P_z2 = point2find2_CF.z;
	//�������η�����ת���õ���������ϵ������OcP��ֵ
	PNPSolver::CodeRotateByZ(Oc2P_x2, Oc2P_y2, p4psolver2.Theta_W2C.z, Oc2P_x2, Oc2P_y2);
	PNPSolver::CodeRotateByY(Oc2P_x2, Oc2P_z2, p4psolver2.Theta_W2C.y, Oc2P_x2, Oc2P_z2);
	PNPSolver::CodeRotateByX(Oc2P_y2, Oc2P_z2, p4psolver2.Theta_W2C.x, Oc2P_y2, Oc2P_z2);
	//����ȷ��һ��ֱ��
	cv::Point3f b1(p4psolver2.Position_OcInW.x, p4psolver2.Position_OcInW.y, p4psolver2.Position_OcInW.z);
	cv::Point3f b2(p4psolver2.Position_OcInW.x + Oc2P_x2, p4psolver2.Position_OcInW.y + Oc2P_y2, p4psolver2.Position_OcInW.z + Oc2P_z2);








	/*************************���P������**************************/
	//�������ǻ���˹��ڵ�P������ֱ��a1a2��b1b2
	//������ֱ�ߵĽ�����ǵ�P��λ��
	//�����ڴ��ڲ���������ֱ�߲��������غϵģ������˶������
	//�������ֱ������ĵ㣬����P���ڵ�λ���ˡ�

	GetDistanceOf2linesIn3D g;//��ʼ��
	g.SetLineA(a1.x, a1.y, a1.z, a2.x, a2.y, a2.z);//����ֱ��A�ϵ�����������
	g.SetLineB(b1.x, b1.y, b1.z, b2.x, b2.y, b2.z);//����ֱ��B�ϵ�����������
	g.GetDistance();//�������
	double d = g.distance;//��þ���
	//��PonA��PonB�ֱ�Ϊֱ��A��B����ӽ��ĵ㣬���ǵ��е����P������
	double x = (g.PonA_x + g.PonB_x) / 2;
	double y = (g.PonA_y + g.PonB_y) / 2;
	double z = (g.PonA_z + g.PonB_z) / 2;




	return cv::Point3f(x, y, z);
}


//������ͨ������ͼ��λ�ˣ����δ֪��P�Ŀռ����꣨�������꣩
//@Author��VShawn
//@URL��http://www.cnblogs.com/singlex/
//��ϸԭ����˵����
int main()
{
	/*************��ʼ���������***********/

	//����ڲ���
	double camD[9] = {
		6800.7, 0, 3065.8,
		0, 6798.1, 1667.6,
		0, 0, 1 };

	double fx = camD[0];
	double fy = camD[4];
	double u0 = camD[2];
	double v0 = camD[5];

	//��ͷ�������
	double k1 = -0.189314;
	double k2 = 0.444657;
	double p1 = -0.00116176;
	double p2 = 0.00164877;
	double k3 = -2.57547;



	/********��һ��ͼ********/
	PNPSolver p4psolver1;
	//��ʼ���������
	p4psolver1.SetCameraMatrix(fx, fy, u0, v0);
	//���û������
	p4psolver1.SetDistortionCoefficients(k1, k2, p1, p2, k3);

	p4psolver1.Points3D.push_back(cv::Point3f(0, 0, 0));		//P1��ά����ĵ�λ�Ǻ���
	p4psolver1.Points3D.push_back(cv::Point3f(0, 200, 0));		//P2
	p4psolver1.Points3D.push_back(cv::Point3f(150, 0, 0));		//P3
	p4psolver1.Points3D.push_back(cv::Point3f(150, 200, 0));	//P4
	//p4psolver1.Points3D.push_back(cv::Point3f(0, 100, 105));	//P5

	cout << "�������������� = " << endl << p4psolver1.Points3D << endl << endl << endl;

	//���ͼһ�м���������������P������
	//cv::Mat img1 = cv::imread("1.jpg");
	p4psolver1.Points2D.push_back(cv::Point2f(2985, 1688));	//P1
	p4psolver1.Points2D.push_back(cv::Point2f(5081, 1690));	//P2
	p4psolver1.Points2D.push_back(cv::Point2f(2997, 2797));	//P3
	p4psolver1.Points2D.push_back(cv::Point2f(5544, 2757));	//P4
	//p4psolver1.Points2D.push_back(cv::Point2f(4148, 673));	//P5

	cout << "ͼһ������������ = " << endl << p4psolver1.Points2D << endl;


	if (p4psolver1.Solve(PNPSolver::METHOD::CV_P3P) != 0)
		return -1;

	cout << "ͼһ�����λ��" << endl << "Oc����=" << p4psolver1.Position_OcInW << "      �����ת=" << p4psolver1.Theta_W2C << endl;
	cout << endl << endl;
	/**********************/











	/********��2��ͼ********/
	PNPSolver p4psolver2;
	//��ʼ���������
	p4psolver2.SetCameraMatrix(fx, fy, u0, v0);
	//�������
	p4psolver2.SetDistortionCoefficients(k1, k2, p1, p2, k3);

	p4psolver2.Points3D.push_back(cv::Point3f(0, 0, 0));		//��ά����ĵ�λ�Ǻ���
	p4psolver2.Points3D.push_back(cv::Point3f(0, 200, 0));		//P2
	p4psolver2.Points3D.push_back(cv::Point3f(150, 0, 0));		//P3
	p4psolver2.Points3D.push_back(cv::Point3f(150, 200, 0));	//P4
	//p4psolver2.Points3D.push_back(cv::Point3f(0, 100, 105));	//P5

	//���ͼ���м���������������P������
	//cv::Mat img2 = cv::imread("2.jpg");
	p4psolver2.Points2D.push_back(cv::Point2f(3062, 3073));	//P1
	p4psolver2.Points2D.push_back(cv::Point2f(3809, 3089));	//P2
	p4psolver2.Points2D.push_back(cv::Point2f(3035, 3208));	//P3
	p4psolver2.Points2D.push_back(cv::Point2f(3838, 3217));	//P4
	//p4psolver2.Points2D.push_back(cv::Point2f(3439, 2691));	//P5
	cout << "ͼ�������������� = " << endl << p4psolver2.Points2D << endl;
	if (p4psolver2.Solve(PNPSolver::METHOD::CV_P3P) != 0)
		return -1;
	cout << "ͼ�������λ��" << endl << "Oc����=" << p4psolver2.Position_OcInW << "      �����ת=" << p4psolver2.Theta_W2C << endl;

	/**********************/









	cv::Point2f point2find1_IF = cv::Point2f(4149, 671);//�����P��ͼ1������
	cv::Point2f point2find2_IF = cv::Point2f(3439, 2691);//�����P��ͼ2������


	cv::Point3f p = GetPointInWorld(point2find1_IF, p4psolver1, point2find2_IF, p4psolver2);
	cout << endl << "-------------------------------------------------------------" << endl;
	cout << "���P�������� = (" << p.x << "," << p.y << "," << p.z << ")" << endl;



	//ע��Ϊ�˸���ȷ�ļ�����ռ����꣬���Լ��������P��λ�ã���ȡ���ǵ�����
	//End @VShawn(http://www.cnblogs.com/singlex/)
	return 0;
}