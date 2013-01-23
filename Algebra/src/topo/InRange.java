package topo;

import field.DoubleField;

/**
 * The 'in range' relation: that is two elements are related if and only if both are
 * element of the same interval
 * @author bzfmuell
 *
 */
public class InRange extends AbstractRelation<DoubleField, InRange> {
	
	/**
	 * Constructs a new range relation: any two elements
	 * @param lower
	 * @param upper
	 */
	public InRange (DoubleField lower, DoubleField upper){
		super();
		basePoint = new PairedElement<DoubleField> (lower,upper);
	}
	
	public boolean isEmpty() {return basePoint.getFirst().compareTo(basePoint.getSecond())<=0;}

	
	public boolean isOpen() {return isEmpty()?true:false;}

	
	public boolean isClosed() {return true;}

	
	public boolean isRelated(DoubleField first, DoubleField second) {
		DoubleField lower = basePoint.getFirst(), upper = basePoint.getSecond();
		return lower.compareTo(first)<=0&&first.compareTo(upper)<=0&&lower.compareTo(second)<=0&&second.compareTo(upper)<=0;
	}

}
