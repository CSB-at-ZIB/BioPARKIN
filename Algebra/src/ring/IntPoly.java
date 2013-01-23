package ring;

import java.util.Iterator;
import java.util.Map;

import ring.Poly.GenPoly;

public class IntPoly extends GenPoly<IntRing> {
	/**
	 * Constructs the zero polynomial
	 */
	public IntPoly (){
		super();
	}
	/**
	 * Constructs the monomial <tt>coeff * X^index</tt>
	 * @param index the degree of the monomial
	 * @param coeff the coefficient
	 */
	public IntPoly (int index, IntRing coeff){
		super(index,coeff);
	}
	/**
	 * Constructs the polynomial <p><tt>coeffArray[0] + coeffArray[1] X + ... + coeffArray[n-1] X^(n-1)</tt>,</p> where
	 * <tt>n</tt> equals the length of the array
	 * @param coeffArray the coefficient array
	 */
	public IntPoly (int[] coeffArray){
		super();
		for (int i = 0; i < coeffArray.length; i++) {
			if(coeffArray[i]==0) continue;
			setCoefficient (i, new IntRing (coeffArray[i]));
		}
	}
	/**
	 * Constructs the polynomial <p><tt>coeffArray[0] + coeffArray[1] X + ... + coeffArray[n-1] X^(n-1)</tt>,</p> where
	 * <tt>n</tt> equals the length of the array
	 * @param coeffArray the coefficient array
	 */
	public IntPoly (IntRing[] coeffArray){
		super(coeffArray);
	}
	/**
	 * Copies the argument polynomial <tt>another</tt>
	 * @param another some other polynomial
	 */
	public IntPoly (Poly<IntRing> another){
		super(another);
	}
	public IntPoly add(Poly<IntRing> another) {
		IntPoly sum = new IntPoly ();
		for (Map.Entry<Integer, IntRing> entries:this) sum.setCoefficient(entries.getKey(), entries.getValue());
		for (Map.Entry<Integer, IntRing> entries:another) {
			Integer index = entries.getKey();
			IntRing curr = sum.getCoefficient(index);
			if(curr==null) sum.setCoefficient(index, entries.getValue());
			else {
				curr = curr.add(entries.getValue());
				if(!curr.isZero()) sum.setCoefficient(index, curr);
				else sum.removeCoefficient(index);
			}
		}
		return sum;
	}

	
	public IntPoly addInverse() {
		IntPoly inv = new IntPoly ();
		for (Map.Entry<Integer, IntRing> entries:this) inv.setCoefficient(entries.getKey(), entries.getValue().addInverse());
		return inv;
	}
	public boolean equals (Poly<IntRing> another){return equals((Object) another);}
	
	public boolean equals (Object o){
		if(this==o) return true;
		if(!(o instanceof IntPoly)) return false;
		IntPoly cp = (IntPoly) o;
		Iterator<Map.Entry<Integer,IntRing>> it1 = iterator();
		Iterator<Map.Entry<Integer,IntRing>> it2 = cp.iterator();
		while (it1.hasNext()&&it2.hasNext()){
			Map.Entry<Integer, IntRing> entry1 = it1.next();
			Map.Entry<Integer, IntRing> entry2 = it2.next();
			if(!entry1.equals(entry2)) return false;
		}
		if(it1.hasNext()||it2.hasNext()) return false;
		return true;
	}
	public IntRing eval (IntRing arg){
		if(isZero()) return new IntRing ();
		int deg = degree();
		if(deg==0) return new IntRing (getCoefficient(deg));
		IntRing val = new IntRing ();
		IntRing arG = new IntRing (1);
		int count = 0;
		for (Map.Entry<Integer, IntRing> entries:this) {
			int index = entries.getKey();
			IntRing coeff = entries.getValue();
			while (count<index){
				arG = arG.multiply(arg);
				count++;
			}
			val = val.add(coeff.multiply(arG));
		}
		return val;
	}
	public boolean isCommutative (){return true;}
	public IntPoly multiply(Poly<IntRing> another) {
		IntPoly prod = new IntPoly ();
		for (Map.Entry<Integer, IntRing> entries1:this){
			int index1 = entries1.getKey();
			IntRing coeff1 = entries1.getValue();
			for (Map.Entry<Integer, IntRing> entries2:another){
				int index2 = entries2.getKey();
				int nIndex = index1+index2;
				IntRing coeff2 = entries2.getValue();
				IntRing c1TimesC2 = coeff1.multiply(coeff2);
				IntRing entry = null;
				if((entry = prod.getCoefficient(nIndex))==null) prod.setCoefficient(nIndex, c1TimesC2);
				else {
					entry = entry.add(c1TimesC2);
					if(!entry.isZero()) prod.setCoefficient(nIndex, entry);
					else prod.removeCoefficient(nIndex);
				}
			}
		}
		return prod;
	}
	public static void main (String[] args){
		IntPoly p1 = new IntPoly (new int[]{1,0,0,-1});
		p1 = p1.multiply(new IntPoly(new int[]{2,-1,3}));
		IntRing arg = new IntRing(12);
		long start1 = System.nanoTime();
		IntRing val1 = p1.eval(arg);
		long end1  = System.nanoTime();
		System.out.println("normal eval: "+val1+"\texe time: "+((double) end1-start1)*1e-9);
		System.out.println(p1);
	}
}
