#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <random>
#include <map>
#include <time.h>
#include <stdlib.h>
using namespace std;

int sampling(int n, int ml, string input_name, string output_name, int k);

int main (int argc, char *argv[]) {
        int k = 4;
        int n = atoi(argv[3]);
        int ml = atoi(argv[4]);
        string input_name = argv[1];
        string output_name = argv[2];
        int n_reads_written = sampling(n,ml,input_name,output_name,k);

        float target_factor = ((float)ml)/n;
        float actual_factor = ((float)n_reads_written)/n;
        cout << "ml=" << ml << " -- n_reads_written=" << n_reads_written << "\n";
        cout << "target_factor=" << target_factor << " -- actual_factor=" << actual_factor << "\n";

        return 0;
}

int sampling(int n, int ml, string input_name, string output_name, int k){
    int n_current = n;
    int ml_current = ml;
    std::default_random_engine generator;
    fstream input;
    input.open(input_name,ios::in);
    fstream output;
    output.open(output_name,ios::out);
    int n_reads_written = 0;
    srand(time(NULL));

    while(n_current > 0 && ml_current > 0){
        std::binomial_distribution<int> binomial_distr(ml_current,std:: min(1.0,double(k)/double(n_current)));
        int c = binomial_distr(generator);
        //ml_current -= c;
        //n_current -= k;
        std::map<int, int> s;
	int k_adjusted = int(min(k,n_current));
        for(int i = 0; i < c; i++){
            int random_index = rand()%k_adjusted+1;
            if(s.count(random_index)==0)
                s[random_index] = 1;
            else
                s[random_index] += 1;
        }
        for(int i = 1; i <= k_adjusted; i++){
            //load next read
            string seq_id;
            string read;
            string plus_line;
            string quality;
            getline(input, seq_id);
            getline(input, read);
            getline(input, plus_line);
            getline(input, quality);

            int r_i = 0;
            if(s.count(i)==1)
                r_i = s[i];

            for(int j = 0 ; j < r_i ; j++){
                output << seq_id + "\n";
                output << read + "\n";
                output << plus_line + "\n";
                output << quality + "\n";
                n_reads_written += 1;
            }
        }
        ml_current -= c;
        n_current -= k_adjusted;
    }
    input.close();
    output.close();
    return n_reads_written;
}
