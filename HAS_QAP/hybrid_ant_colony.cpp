#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <numeric> // iota
#include <random>
#include <algorithm> // shuffle, sort
#include <chrono>
#include <limits>
#include <thread> // TODO
#include <random>
#include <ctime>

/**
	Functions declarations, see function implementations for documentation
*/
void open_qap(std::string path, int &size, std::vector<std::vector<int>> &distances, std::vector<std::vector<int>> &flows);
void reinitialize();
std::vector<std::vector<int>> generate_permutation(int N);
void init_pheromones();
void evaporate_pheromones();
void drop_pheromones(std::vector<int> s);
int cost_function(std::vector<int> s);
int swap_cost_function(std::vector<int> s, int i, int j);
void local_search(std::vector<int> &permutation);
void ant(std::vector<int> &permutation);
void pheromone_trail_based_swap(std::vector<int> &permutation);
std::vector<float> compute_probabilites(std::vector<int> permutation, int r);
void swap_by_indexes(std::vector<int> &v, int i, int j);
bool compare_by_cost(std::vector<int> v1, std::vector<int> v2);
int total_cost();
unsigned generate_seed();
float total_time();

/**
	To delete when done implementing
*/
void print_vector(std::vector<int> v);
void print_2_dim_vector(std::vector<std::vector<int>> v);

/**
	For time recording purpose
*/
std::clock_t begin;

/**
 	Max computation time
*/
float max_computation_time=1.0;

/**
	Random related variables
*/
std::default_random_engine generator(generate_seed());
std::uniform_real_distribution<> zero_to_one(0.0,1.0);

/**
	Number of ants
*/
const int N=10;

/**
	Parameter used for initializing the pheromones matrix
*/
const int Q=100;

/**
	Parameter for ant swap decision	
*/
const float q=0.9;

/**
	Parameter for pheromones decaying
*/
const float a_1=0.1;

/**
	Parameter for pheromones updating
*/
const float a_2=0.1;

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
	intensification trigger
*/
bool intensification=true;

/**
 	True if first pass, or just reinitialized
*/
bool first=true;

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

/**
 	Pheromones matrix
*/
std::vector<std::vector<float>> pheromones;

/**
	Sum of the previous solution held by the ants, for comparing purpose, sum is a strong enough criteria
*/
int previous_costs=std::numeric_limits<int>::max();

/**
	All the threads running the ants
*/
std::thread threads[N];


int main(int argc, char** argv)
{
	//========== INIT ==========
	begin = clock();

	if(argc<1)
	{
		std::cout << "ant_colony must be fed at least one argument :\n- path : the relative or absolute path to the .dat file describing the QAP\n- (OPTIONAL) maxtime : max computation time (in seconds), default=60" << std::flush;
		return 1;
	}

	else
	{
		open_qap(argv[1],size,distances,flows);
		if(argc>1)
		{
			max_computation_time=(std::atoi(argv[2]));
		}
	}
	S_max=(int)size/2.0;
	R=(int)size/3.0;

	permutations=generate_permutation(N);

	for(auto &permutation : permutations)
	{
		local_search(permutation);
	}
	sort(permutations.begin(), permutations.end(), compare_by_cost);

	all_time_best_permutation=permutations[0];

	init_pheromones();


	//========== MAIN LOOP ==========
	while(total_time()<max_computation_time)
	{
		// Launch ants
		for(int n=0; n<N; n++)
		{	
			ant(permutations[n]);
		}

		// De-activate first
		if(first)
		{
			first=false;
		}

		// Sort every ant's solution
		sort(permutations.begin(), permutations.end(), compare_by_cost);
		std::vector<int> iteration_best_permutation = permutations[0];

		//Trigger intensification if best solution has been improved
		if(cost_function(all_time_best_permutation)>cost_function(iteration_best_permutation))
		{
			S=0;
			if(!intensification)
			{
				std::cout << "==== INTENSIFICATION ON ===" << std::endl << std::flush;
				intensification=true;
			}
		}
		else
		{
			S++;
		}

		// Un-trigger intensification if no ant has improved it's solution (checked by comparing sums of solutions)
		int this_iteration_costs = total_cost();
		if(intensification && this_iteration_costs==previous_costs)
		{
			std::cout << "==== INTENSIFICATION OFF ===" << std::endl << std::flush;
			intensification=false;
		}

		previous_costs=this_iteration_costs;
		all_time_best_permutation=std::min(all_time_best_permutation,iteration_best_permutation,compare_by_cost);

		evaporate_pheromones();

		drop_pheromones(all_time_best_permutation);

		if(S==S_max)
		{
			std::cout << "==== DIVERSIFICATION ===" << std::endl << std::flush;
			reinitialize();
		}

		std::cout << total_time() << "s - All time best permutation : [ " << std::flush;
		for(auto i : all_time_best_permutation)
		{
			std::cout << i << " " << std::flush;
		}
		std::cout << "] at cost : " << cost_function(all_time_best_permutation) << " - this iteration best : " << cost_function(iteration_best_permutation) << std::endl << std::flush;
	}
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
	Reinitialize everything for diversification purpose, only keeping all_time_best_solution
*/
void reinitialize()
{
	permutations=generate_permutation(N-1);
	permutations.push_back(all_time_best_permutation);
	sort(permutations.begin(), permutations.end(), compare_by_cost);

	init_pheromones();

	intensification=true;

	S=0;

	first=true;
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

		std::shuffle(tmp.begin(), tmp.end(), generator);

		generated_permutations.push_back(tmp);
	}
	return generated_permutations;
}

/**
	Initializes the pheromones matrix
*/
void init_pheromones()
{
	pheromones.clear();
	for(int i=0; i<size; i++)
	{
		std::vector<float> tmp(size);
		std::fill(tmp.begin(), tmp.end(), 1.0/(Q*cost_function(all_time_best_permutation)));
		pheromones.push_back(tmp);
	}
}

/**
	Decays pheromones
*/
void evaporate_pheromones()
{
	for(int i=0; i<size; i++)
	{
		for(int j=0; j<size; j++)
		{
			pheromones[i][j]*=(1-a_1);
		}
	}
}

/**
	Alters the pheromone matrix according to solution s
*/ 
void drop_pheromones(std::vector<int> s)
{
	int c = cost_function(s);
	for(int i=0; i<size; i++)
	{
		pheromones[i][s[i]]+=(a_2/c);
	}
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
		for(auto i : (std::vector<int>) generate_permutation(1)[0])
		{
			for(auto j : (std::vector<int>) generate_permutation(1)[0])
			{
				if(i==j)
				{
					continue;
				}
				if (swap_cost_function(s,i,j)<0)
				{
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
	Ant
*/
void ant(std::vector<int> &permutation)
{
	if(!first)
	{
		local_search(permutation);
	}
	std::vector<int> prev_permutation = permutation;
	int prev_cost=cost_function(prev_permutation);

	for(int reps=0; reps<R; reps++)
	{
		pheromone_trail_based_swap(permutation);
		local_search(permutation);
	}
	if(intensification and prev_cost<cost_function(permutation))
	{
		permutation=prev_permutation;
	}
}

/**
 	Performs a swap in permutation based on the pheromones trail
*/
void pheromone_trail_based_swap(std::vector<int> &permutation)
{
	std::uniform_int_distribution<> choser(0,size-1);
	int r = choser(generator);
	int s;
	std::vector<float> probs = compute_probabilites(permutation, r);
	if(zero_to_one(generator)>(1-q))
	{
		std::vector<int> all_s;
		float max_prob=0;
		for(int i=0; i<probs.size(); i++)
		{
			if(probs[i]>max_prob)
			{
				all_s.clear();
				all_s.push_back(i);
				max_prob=probs[i];
			}
			else if(probs[i]==max_prob)
			{
				all_s.push_back(i);
			}
		}
		s=all_s[((int) zero_to_one(generator)*all_s.size())%all_s.size()];
	}
	else
	{
		float chosen = zero_to_one(generator);
		float prob_sum=0;
		for(int i=0; i<probs.size(); i++)
		{
			prob_sum+=probs[i];
			if(prob_sum>chosen)
			{
				s=i;
				break;
			}
		}
	}
	swap_by_indexes(permutation,r,s);
}

std::vector<float> compute_probabilites(std::vector<int> permutation, int r)
{
	std::vector<float> probs(size);
	float sum=0;

	for(auto element : permutation)
	{
		if(element==r)
		{
			probs[element]=0.0;
		}
		probs[element]=pheromones[r][permutation[element]]+pheromones[element][permutation[r]];
		sum+=probs[element];
	}

	for(auto &prob : probs)
	{
		prob=prob/sum;
	}

	return probs;
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

/**
	Compute the total cost of current solutions (for comparing purpose)
*/
int total_cost()
{
	int total_cost = 0;
	for(auto permutation : permutations)
	{
		total_cost+=cost_function(permutation);
	}
	return total_cost;
}

/**
	Generate a random seed based on current time
*/
unsigned generate_seed()
{
	return std::chrono::system_clock::now().time_since_epoch().count();
}

/**
	Keeps track of how many seconds have elapsed since the ant colony is running
*/
float total_time()
{
	std::clock_t now = std::clock();

	float current_total_time = float(now-begin) / CLOCKS_PER_SEC;

	return current_total_time;
}


void print_vector(std::vector<int> v)
{
	for(auto elem : v)
	{
		std::cout << elem << " " << std::flush;
	}
	std::cout << cost_function(v) << std::endl << std::flush;
}

void print_2_dim_vector(std::vector<std::vector<int>> v)
{
	for(auto vector : v)
	{
		print_vector(vector);
	}
	std::cout << std::endl << std::flush;
}