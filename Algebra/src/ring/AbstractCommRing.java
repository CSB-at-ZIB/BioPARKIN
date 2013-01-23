package ring;

public abstract class AbstractCommRing<A extends AbstractCommRing<A>> extends
		RingElement<A> {
	public AbstractCommRing (){super();}
	public boolean isCommutative (){return true;}
}
