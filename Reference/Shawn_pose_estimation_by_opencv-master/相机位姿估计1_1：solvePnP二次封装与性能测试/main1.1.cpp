#include "stdafx.h"

#include "..\include\PNPSolver.h"

//�������ڲ��Զ�opencv��solvePNP�����Ķ��η�װ��PNPSolver
//@Author��VShawn
//@URL��http://www.cnblogs.com/singlex/

/*************����������***********/
//�ڲ���
double fx = 6800.7;
double fy = 6798.1;
double u0 = 3065.8;
double v0 = 1667.6;
//��ͷ�������
double k1 = -0.189314;
double k2 = 0.444657;
double p1 = -0.00116176;
double p2 = 0.00164877;
double k3 = -2.57547;

void test1();
void test2();
void test3();
void test4();

int main()
{
	//���Թ���4������
	test1();

	cout << endl << endl << endl << endl << endl << endl << endl << endl;

	//�ǹ����ĵ����λ��
	test2();

	cout << endl << endl << endl << endl << endl << endl << endl << endl;

	//��5�������λ��
	test3();

	cout << endl << endl << endl << endl << endl << endl << endl << endl;

	//���ַ����ٶȲ���
	test4();
	return 0;
}

void test1()
{
	cout << "test1:�ĵ㹲��" << endl;
	//��ʼ��PNPSolver��
	PNPSolver p4psolver;
	//��ʼ���������
	p4psolver.SetCameraMatrix(fx, fy, u0, v0);
	//���û������
	p4psolver.SetDistortionCoefficients(k1, k2, p1, p2, k3);

	p4psolver.Points3D.push_back(cv::Point3f(0, 0, 0));		//P1��ά����ĵ�λ�Ǻ���
	p4psolver.Points3D.push_back(cv::Point3f(0, 200, 0));	//P2
	p4psolver.Points3D.push_back(cv::Point3f(150, 0, 0));	//P3
	p4psolver.Points3D.push_back(cv::Point3f(150, 200, 0));	//P4
	//p4psolver.Points3D.push_back(cv::Point3f(0, 100, 105));	//P5

	cout << "test1:�������������� = " << endl << p4psolver.Points3D << endl;

	p4psolver.Points2D.push_back(cv::Point2f(2985, 1688));	//P1
	p4psolver.Points2D.push_back(cv::Point2f(5081, 1690));	//P2
	p4psolver.Points2D.push_back(cv::Point2f(2997, 2797));	//P3
	p4psolver.Points2D.push_back(cv::Point2f(5544, 2757));	//P4
	//p4psolver.Points2D.push_back(cv::Point2f(4148, 673));	//P5

	cout << "test1:ͼ������������ = " << endl << p4psolver.Points2D << endl;

	if (p4psolver.Solve(PNPSolver::METHOD::CV_P3P) == 0)
		cout << "test1:CV_P3P����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;
	if (p4psolver.Solve(PNPSolver::METHOD::CV_ITERATIVE) == 0)
		cout << "test1:CV_ITERATIVE����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;
	if (p4psolver.Solve(PNPSolver::METHOD::CV_EPNP) == 0)
		cout << "test1:CV_EPNP����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;

	return;
}


void test2()
{
	cout << "test2:�ĵ㲻����" << endl;
	//��ʼ��PNPSolver��
	PNPSolver p4psolver;
	//��ʼ���������
	p4psolver.SetCameraMatrix(fx, fy, u0, v0);
	//���û������
	p4psolver.SetDistortionCoefficients(k1, k2, p1, p2, k3);

	p4psolver.Points3D.push_back(cv::Point3f(0, 0, 0));		//P1��ά����ĵ�λ�Ǻ���
	p4psolver.Points3D.push_back(cv::Point3f(0, 200, 0));	//P2
	p4psolver.Points3D.push_back(cv::Point3f(150, 0, 0));	//P3
	//p4psolver.Points3D.push_back(cv::Point3f(150, 200, 0));	//P4
	p4psolver.Points3D.push_back(cv::Point3f(0, 100, 105));	//P5

	cout << "test2:�������������� = " << endl << p4psolver.Points3D << endl;

	p4psolver.Points2D.push_back(cv::Point2f(2985, 1688));	//P1
	p4psolver.Points2D.push_back(cv::Point2f(5081, 1690));	//P2
	p4psolver.Points2D.push_back(cv::Point2f(2997, 2797));	//P3
	//p4psolver.Points2D.push_back(cv::Point2f(5544, 2757));	//P4
	p4psolver.Points2D.push_back(cv::Point2f(4148, 673));	//P5

	cout << "test2:ͼ������������ = " << endl << p4psolver.Points2D << endl;

	if (p4psolver.Solve(PNPSolver::METHOD::CV_P3P) == 0)
		cout << "test2:CV_P3P����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;
	if (p4psolver.Solve(PNPSolver::METHOD::CV_ITERATIVE) == 0)
		cout << "test2:CV_ITERATIVE����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;
	if (p4psolver.Solve(PNPSolver::METHOD::CV_EPNP) == 0)
		cout << "test2:CV_EPNP����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;

	return;
}

void test3()
{
	cout << "test3:������" << endl;
	//��ʼ��PNPSolver��
	PNPSolver p4psolver;
	//��ʼ���������
	p4psolver.SetCameraMatrix(fx, fy, u0, v0);
	//���û������
	p4psolver.SetDistortionCoefficients(k1, k2, p1, p2, k3);

	p4psolver.Points3D.push_back(cv::Point3f(0, 0, 0));		//P1��ά����ĵ�λ�Ǻ���
	p4psolver.Points3D.push_back(cv::Point3f(0, 200, 0));	//P2
	p4psolver.Points3D.push_back(cv::Point3f(150, 0, 0));	//P3
	p4psolver.Points3D.push_back(cv::Point3f(150, 200, 0));	//P4
	p4psolver.Points3D.push_back(cv::Point3f(0, 100, 105));	//P5

	cout << "test3:�������������� = " << endl << p4psolver.Points3D << endl;

	p4psolver.Points2D.push_back(cv::Point2f(2985, 1688));	//P1
	p4psolver.Points2D.push_back(cv::Point2f(5081, 1690));	//P2
	p4psolver.Points2D.push_back(cv::Point2f(2997, 2797));	//P3
	p4psolver.Points2D.push_back(cv::Point2f(5544, 2757));	//P4
	p4psolver.Points2D.push_back(cv::Point2f(4148, 673));	//P5

	cout << "test3:ͼ������������ = " << endl << p4psolver.Points2D << endl;

	if (p4psolver.Solve(PNPSolver::METHOD::CV_P3P) == 0)
		cout << "test3:CV_P3P����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;
	if (p4psolver.Solve(PNPSolver::METHOD::CV_ITERATIVE) == 0)
		cout << "test3:CV_ITERATIVE����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;
	if (p4psolver.Solve(PNPSolver::METHOD::CV_EPNP) == 0)
		cout << "test3:CV_EPNP����:	���λ�ˡ�" << "Oc����=" << p4psolver.Position_OcInW << "	�����ת=" << p4psolver.Theta_W2C << endl;

	return;
}

void test4()
{
	cout << "test4:�㷨�ٶȲ���" << endl;
	//��ʼ��PNPSolver��
	PNPSolver p4psolver;
	//��ʼ���������
	p4psolver.SetCameraMatrix(fx, fy, u0, v0);
	//���û������
	p4psolver.SetDistortionCoefficients(k1, k2, p1, p2, k3);

	p4psolver.Points3D.push_back(cv::Point3f(0, 0, 0));		//P1��ά����ĵ�λ�Ǻ���
	p4psolver.Points3D.push_back(cv::Point3f(0, 200, 0));	//P2
	p4psolver.Points3D.push_back(cv::Point3f(150, 0, 0));	//P3
	p4psolver.Points3D.push_back(cv::Point3f(150, 200, 0));	//P4
	//p4psolver.Points3D.push_back(cv::Point3f(0, 100, 105));	//P5

	//cout << "test1:�������������� = " << endl << p4psolver.Points3D << endl;

	p4psolver.Points2D.push_back(cv::Point2f(2985, 1688));	//P1
	p4psolver.Points2D.push_back(cv::Point2f(5081, 1690));	//P2
	p4psolver.Points2D.push_back(cv::Point2f(2997, 2797));	//P3
	p4psolver.Points2D.push_back(cv::Point2f(5544, 2757));	//P4
	//p4psolver.Points2D.push_back(cv::Point2f(4148, 673));	//P5

	//cout << "test1:ͼ������������ = " << endl << p4psolver.Points2D << endl;

	double t = cv::getTickCount();
	for (int i = 0; i < 1000; i++)
	{
		p4psolver.Solve(PNPSolver::METHOD::CV_P3P);
	}
	cout << "test4:CV_P3P����ִ��1000����ʱ:				" << (cv::getTickCount() - t) / cv::getTickFrequency() * 1000 << "ms" << endl;

	t = cv::getTickCount();
	for (int i = 0; i < 1000; i++)
	{
		p4psolver.Solve(PNPSolver::METHOD::CV_ITERATIVE);
	}
	cout << "test4:CV_ITERATIVE����ִ��1000����ʱ:			" << (cv::getTickCount() - t) / cv::getTickFrequency() * 1000 << "ms" << endl;

	t = cv::getTickCount();
	for (int i = 0; i < 1000; i++)
	{
		p4psolver.Solve(PNPSolver::METHOD::CV_EPNP);
	}
	cout << "test4:CV_EPNP����ִ��1000����ʱ:			" << (cv::getTickCount() - t) / cv::getTickFrequency() * 1000 << "ms" << endl;

	return;
}