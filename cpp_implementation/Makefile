CXX=g++
CXXFLAGS=-std=c++11 -march=native -O3 -DNDEBUG

bc: graph_loader.o bc.o brandes.o
	$(CXX) $(CXXFLAGS) -o $@ $^

.PHONY:
clean:
	rm -f *.o bc
