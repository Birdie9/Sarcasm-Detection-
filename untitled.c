#include<stdio.h>
using namespace std;
int main()
{
	int t,n;
	cin>>t;
	for(int i=0;i<t;i++)
		cin>>n;
	if(n%2==0)
		cout<<n/2;
	else cout<<(n+1)/2;
	return 0;

}