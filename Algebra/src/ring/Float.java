package ring;

import java.util.Map;
import java.util.TreeMap;
//TODO implement class!!!
public class Float extends AbstractCommRing<Float>{
	private TreeMap<Integer,Object> valueMap;
	/**the number of trailing (post comma) values*/
	private int trailingFloats;
	private int modCount;
	public Float (){super();valueMap = new TreeMap<Integer,Object> ();}
	public Float (float value){this((double) value);}
	public Float (double value){
		this(20,5);
		constructVal(value);
	}
	public Float (int trailingFloats, int modCount){
		this();
		this.modCount       = modCount;
		this.trailingFloats = trailingFloats;
		
	}
	public Float addInverse() {
		// TODO Auto-generated method stub
		return null;
	}
	public boolean isZero() {return valueMap.size()==0?true:false;}
	public Float multiply(Float another) {
		// TODO Auto-generated method stub
		return null;
	}
	public Float add(Float another) {
		if(modCount!=another.modCount) throw new IllegalArgumentException ("");
		Float sum = new Float (Math.max(trailingFloats,another.trailingFloats),modCount);
		for (Map.Entry<Integer,Object> entry:valueMap.entrySet()) sum.valueMap.put(entry.getKey(), entry.getValue());
		return sum;
	}
	private void constructVal (double value){
		int counter = 0;
		double cp = value;
		while (counter < trailingFloats){
			if(cp>0) {
				IntRing val1 = new IntRing ((int) Math.floor(cp));
			}
			else {
				
			}
			counter++;
		}
	}
	
	public boolean equals(Float another) {return add(another.addInverse()).isZero()?true:false;}
}
