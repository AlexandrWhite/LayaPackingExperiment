#include <iostream>
#include <vector>
using namespace std;


const int s = 1e6 + 1;
int dp_last[s + 1];
int dp[s + 1];
int w[21];

int main() {
	int n; cin >> n;
	
	int sum = 0;
	for (int i = 1; i <= n; i++) {
		cin >> w[i];
		sum += w[i];
	}	

	for (int i = 0; i <= s; i++) {
		dp_last[i] = 0;
		dp[i] = 0;
	}

	dp_last[0] = 1;

	vector<vector<int>>ans_last(sum/2+1);
	vector<vector<int>>ans(sum/2+1);

	for (int i = 1; i <= n; i++) {
		for (int j = 0; j <= sum/2; j++) {
			if (j < w[i]) {
				dp[j] = dp_last[j];
				ans[j] = ans_last[j];
			}else {
				dp[j] = dp_last[j] || dp_last[ j - w[i] ];
			}
			if (j >= w[i] && dp_last[ j - w[i] ] == 1) {
				ans[j] = ans_last[j - w[i]];
				ans[j].push_back(w[i]);
			}
		}

		for (int i = 0; i <= sum/2; i++) {
			dp_last[i] = dp[i];
			ans_last[i] = ans[i];
		}
	}

	for (int i = sum/2; i >=0; i--) {
		if (dp[i] == 1) {
			cout << "diff: " << sum - 2 * i << "\n";
			cout<<"pile1: ";
			for(int j=0; j < ans[i].size(); j++){
				cout<<ans[i][j]<<" ";
			}
			cout<<"\n";
			return 0;
		}
	}
}