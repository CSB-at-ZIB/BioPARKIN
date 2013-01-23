package group;

import ring.NonAbelGrp;

public abstract class AbstractNACG<N extends NonAbelGrp<N>> implements
		NonAbelGrp<N> {

	public AbstractNACG (){}

	
	public N operate(N another) {return multiply(another);}

}
