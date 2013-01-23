package ring;

import group.AbstractAbel;

public abstract class RingElement<R extends Ring<R>> extends AbstractAbel<R> implements Ring<R> {
	protected boolean isZero;
	public RingElement (){isZero = true;}
}
