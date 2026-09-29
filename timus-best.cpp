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
				ans[j].push_back(i-1);
			}
		}

		for (int i = 0; i <= sum/2; i++) {
			dp_last[i] = dp[i];
			ans_last[i] = ans[i];
		}
	}

	int diff;
	vector<int>b(n, 0);

	for (int i = sum/2; i >=0; i--) {
		if (dp[i] == 1) {
			diff = sum - 2 * i;
			for(int j=0; j < ans[i].size(); j++){
				b[ans[i][j]] = 1;
			}
			break;	
		}
	}

	cout << "{\"diff\": " << diff << ", \"ans\": [";
    for (size_t k = 0; k < b.size(); ++k) {
        if (k) cout << ", ";
        cout << b[k];
    }
    cout << "], \"stones\": [";

    for(int i=1; i <= n; ++i){
        if (w[i-1]) cout << ", ";
        cout<<w[i];
    }
    cout<<"]}\n";

	return 0;
}