#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <numeric> // iota
#include <random>
#include <algorithm> // shuffle
#include <chrono>

#include <typeinfo>

/**
	Functions declarations, see function implementations for documentation
*/
void open_qap(std::string path, int &size, std::vector<std::vector<int>> &distances, std::vector<std::vector<int>> &flows);
std::vector<std::vector<int>> generate_permutation(int N);
int cost_function(std::vector<int> s);
int swap_cost_function(std::vector<int> s, int i, int j);
void local_search(std::vector<int> &permutation);
void swap_by_indexes(std::vector<int> &v, int i, int j);
bool compare_by_cost(std::vector<int> v1, std::vector<int> v2);

void print_vector(std::vector<int> v);
void print_2_dim_vector(std::vector<std::vector<int>> v);

/**
	Number of ants
*/
int N=10;

/**
	Parameter used for initializing the pheromones matrix
*/
int Q=100;

/**
	Parameter for ant swap decision	
*/
float q=0.1;

/**
	First parameter for pheromones updating
*/
float a_1=0.1;

/**
	Second parameter for pheromones updating
*/
float a_2=0.1;

/**
	Number of swaps that ants have to perform	
*/
int R;

/**
	Max number of iteration where no better solution has been detected before applying a diversification
*/
int S_max;

/**
	Current iteration where no better solution has been detected counter
*/
int S=0;

/**
	Size of the QAP	
*/
int size;

/**
	Distances matrix of the QAP	
*/
std::vector<std::vector<int>> distances;

/**
	Flows matrix of the QAP	
*/
std::vector<std::vector<int>> flows;

/**
	Current permutations held by the ants
*/
std::vector<std::vector<int>> permutations;

/**
	Current best solution found
*/
std::vector<int> all_time_best_permutation;


int main(int argc, char* argv[])
{
	open_qap("../instances/nug12.dat", size, distances, flows);
	S_max=(int)size/2.0;
	R=(int)size/3.0;

	permutations=generate_permutation(N);

	std::vector<int> v = generate_permutation(1)[0];
	std::cout << "v : ";
	print_vector(v);

	print_2_dim_vector(permutations);
	std::cout << "iterating : " << std::endl;
	for(auto permutation : permutations)
	{
		print_vector(permutation);
		std::cout << " . " << std::endl;
		local_search(permutation);
	}
	std::cout << std::endl;

	print_2_dim_vector(permutations);

	sort(permutations.begin(), permutations.end(), compare_by_cost);

	print_2_dim_vector(permutations);

	all_time_best_permutation=permutations[0];
}

/**
	Opens a file containing 2*(size)²+1 integers, the first one being size, and the 2*(size)² next ones describing th two matrixes for a QAP (distances then flows)
*/
void open_qap(std::string path, int &size, std::vector<std::vector<int>> &distances, std::vector<std::vector<int>> &flows)
{
	std::fstream qap_file(path,std::ios_base::in);

	qap_file >> size;

	for(int i=0; i<size; i++)
	{
		std::vector<int> tmp;
		for(int j=0; j<size; j++)
		{	
			int d;
			qap_file >> d;
			tmp.push_back(d);
		}
		distances.push_back(tmp);
	}

	for(int i=0; i<size; i++)
	{
		std::vector<int> tmp;
		for(int j=0; j<size; j++)
		{	
			int f;
			qap_file >> f;
			tmp.push_back(f);
		}
		flows.push_back(tmp);
	}
}

/**
 	Generate N random permutation of 'size' first integers
*/
std::vector<std::vector<int>> generate_permutation(int number)
{
	std::vector<std::vector<int>> generated_permutations;
	for(int n=0; n<number; n++)
	{
		std::vector<int> tmp(size);
		std::iota(tmp.begin(), tmp.end(),0);

		unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();

		std::shuffle(tmp.begin(), tmp.end(), std::default_random_engine(seed));

		generated_permutations.push_back(tmp);
	}
	return generated_permutations;
}

/**
	Cost function for the solution s
*/
int cost_function(std::vector<int> s)
{
	int cost=0;
	for(int i=0; i<size; i++)
	{
		for(int j=0; j<size; j++)
		{
			cost+=distances[i][j]*flows[s[i]][s[j]];
		}
	}
	return cost;
}


/**
	Shift in cost if we swap i an j in solution s
*/
int swap_cost_function(std::vector<int> s, int i, int j)
{
	int cost=0;
	cost=(distances[i][i]-distances[j][j])*(flows[s[j]][s[j]]-flows[s[i]][s[i]])+(distances[i][j]-distances[j][i])*(flows[s[j]][s[i]]-flows[s[i]][s[j]]);
	for (int k=0; k<s.size(); k++)
	{
		if (k==j || k==i)
		{
			continue;
		}
		cost+=(distances[k][i]-distances[k][j])*(flows[s[k]][s[j]]-flows[s[k]][s[i]])+(distances[i][k]-distances[j][k])*(flows[s[j]][s[k]]-flows[s[i]][s[k]]);
	}
	return cost;
}

/**
	Applies the local search algorithm to a solution s
*/
void local_search(std::vector<int> &s)
{
	std::vector<int> initial_s = s;

	for(int rep=0; rep<2; rep++)
	{
		std::cout << "1st loop ok : " << rep << std::endl;
		for(auto i : generate_permutation(1)[0])
		{
			std::cout << "2nd loop ok : " << i << std::endl;
			for(auto j : generate_permutation(1)[0])
			{
				std::cout << "3rd loop ok : " << j << std::endl;
				if(i==j)
				{
					continue;
				}
				if (swap_cost_function(s,i,j)<0)
				{
					std::cout << swap_cost_function(s,i,j);
					swap_by_indexes(s,i,j);
				}
			}
		}
		if(s==initial_s)
		{
			break;
		}
	}

}

/**
	Swap two elements of vector v given their indexes i and j
*/
void swap_by_indexes(std::vector<int> &v, int i, int j)
{
	int tmp=v[i];
	v[i]=v[j];
	v[j]=tmp;
}

/**
	Compare function for vector sorting
*/
bool compare_by_cost(std::vector<int> v1, std::vector<int> v2)
{
	return cost_function(v1)<cost_function(v2);
}

void print_vector(std::vector<int> v)
{
	for(auto elem : v)
	{
		std::cout << elem << " ";
	}
	std::cout << std::endl;
}

void print_2_dim_vector(std::vector<std::vector<int>> v)
{
	for(auto vector : v)
	{
		print_vector(vector);
	}
	std::cout << std::endl;
}