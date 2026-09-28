#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> w(n + 1);
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        cin >> w[i];
        sum += w[i];
    }

    int target = sum / 2;

    vector<char> dp_last(target + 1, 0), dp(target + 1, 0);
    vector<vector<char>> take(n + 1, vector<char>(target + 1, 0));

    dp_last[0] = 1;

    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= target; ++j) {
            dp[j] = dp_last[j];

            if (j >= w[i] && dp_last[j - w[i]]) {
                dp[j] = 1;
                take[i][j] = 1;
            }
        }

        dp_last = dp;
    }

    int best = target;
    while (best >= 0 && !dp_last[best]) {
        --best;
    }


    vector<int> pile1, pile2;
    int j = best;

    for (int i = n; i >= 1; --i) {
        if (j >= w[i] && take[i][j]) {
            pile1.push_back(i);
            j -= w[i];
        } else {
            pile2.push_back(i);
        }
    }

    vector<int>ans(n, 0);
    for(int k=0;k<pile1.size(); k++){
        ans[pile1[k]] = 1; 
    }


    cout << "{\"diff\": " << sum - 2 * best << ", \"ans\": [";
    for (size_t k = 0; k < ans.size(); ++k) {
        if (k) cout << ", ";
        cout << ans[k];
    }
    cout << "], \"stones\": [";

    for(int i=1; i < w.size(); ++i){
        if (w[i-1]) cout << ", ";
        cout<<w[i];
    }
    cout<<"]}\n";
    return 0;
}