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

	for (int i = 1; i <= n; i++) {
		for (int j = 0; j <= sum/2; j++) {
			if (j < w[i]) {
				dp[j] = dp_last[j];
			}else {
				dp[j] = dp_last[j] || dp_last[ j - w[i] ];
			}
		}

		for (int i = 0; i <= sum/2; i++) {
			dp_last[i] = dp[i];
		}
	}

	for (int i = sum/2; i >=0; i--) {
		if (dp[i] == 1) {
			cout << sum - 2 * i << "\n";
			return 0;
		}
	}
}