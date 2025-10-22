(def fact (dambda (n) (
		if (_<_ n 2) 1
		(_*_ n (fact (_-_ n 1)))
	)))
