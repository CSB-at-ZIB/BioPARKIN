package ring;

import group.AbstractAbel;

import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;
/**
 * The polynomial interface over some arbitrary ring <code>R</code>
 * @author gmueller
 *
 * @param <R> the ring type
 */
public interface Poly<R extends Ring<R>> extends Ring<Poly<R>>, Iterable<Entry<Integer, R>>  {
	/**
	 * Returns either the maximal non negative integer <tt>n</tt>, such that <code>getCoefficient(n).isZero()</code>
	 * returns false, or negative infinity, if no such integer exists (e.g. zero polynomial)
	 * @return the degree of this polynomial
	 */
	public int degree();
	/**
	 * Returns the image of the evaluation homomorphism
	 * <code>f_arg : Poly<R> -> R, f_arg(this) = this(arg)</code>
	 * @param arg the argument
	 * @return the image value
	 */
	public R eval (R arg);
	/**
	 * Returns the coefficient at position specified by <tt>index</tt>
	 * @param index the position index 
	 * @return the coefficient or zero/null
	 */
	public R getCoefficient (int index);
	/**
	 * The generic polynomial ring class
	 * @author gmueller
	 *
	 * @param <R>
	 */
	public static abstract class GenPoly<R extends Ring<R>> extends AbstractAbel<Poly<R>> implements Poly<R> {
		/**the coefficient map - a sorted tree map*/
		private TreeMap<Integer,R> coeffMap;
		/**
		 * Constructs the zero polynomial
		 */
		public GenPoly (){super();coeffMap = new TreeMap<Integer,R> ();}
		/**
		 * Constructs the monomial <tt>coeff * X^index</tt>
		 * @param index the degree of the monomial
		 * @param coeff the coefficient
		 */
		protected GenPoly (int index, R coeff){
			this();
			setCoefficient(index,coeff);
		}
		/**
		 * Constructs the polynomial <p><tt>coeffArray[0] + coeffArray[1] X + ... + coeffArray[n-1] X^(n-1)</tt>,</p> where
		 * <tt>n</tt> equals the length
		 * @param coeffArray the coefficient array
		 */
		protected GenPoly (R[] coeffArray){
			this();
			for (int i = 0; i < coeffArray.length; i++){
				if(coeffArray[i]!=null) setCoefficient(i,coeffArray[i]);
			}
		}
		/**
		 * Copies the argument polynomial <tt>another</tt>
		 * @param another
		 */
		protected GenPoly (Poly<R> another){
			this();
			for (Map.Entry<Integer,R> entries:another) setCoefficient(entries.getKey(),entries.getValue());
		}
		public int degree() {return coeffMap.size()==0?Integer.MIN_VALUE:coeffMap.lastKey();}
		public R getCoefficient(int index) {
			R coeff = coeffMap.get(index);
			return coeff==null?null:coeff;
		}
		
		public boolean isZero() {return coeffMap.size()==0?true:false;}
		/**
		 * Returns an iterator over all position index-coefficient pairs
		 */
		public Iterator<Entry<Integer, R>> iterator() {return coeffMap.entrySet().iterator();}
		/**
		 * Removes the coefficient at position <tt>index</tt> or leaves this
		 * polynomial unaltered, if no such coefficient exist
		 * @param index
		 */
		protected void removeCoefficient (int index){
			coeffMap.remove(index);
		}
		/**
		 * Sets the coefficient of this polynomial to <tt>coeff</tt> at position
		 * specified by the <tt>index</tt> argument
		 * @param index the position index
		 * @param coeff the coefficient
		 * @throws IllegalArgumentException negative index
		 */
		public void setCoefficient (int index, R coeff) throws IllegalArgumentException {
			if(index<0) throw new IllegalArgumentException ("\nNegative indices NOT permitted: "+index);
			if(coeff!=null&&!coeff.isZero()) coeffMap.put(index, coeff);
		}
		@Override
		public String toString (){
			StringBuilder sb = new StringBuilder ();
			Iterator<Map.Entry<Integer, R>> it = iterator();
			String format = "%1$s X^%2$d";
			String plus   = " + ";
			while (it.hasNext()){
				Map.Entry<Integer, R> entry = it.next();
				int index = entry.getKey();
				R coeff   = entry.getValue();
				if(index==0) sb.append(coeff.toString());
				if(index==1) sb.append(String.format("%1$s X",coeff.toString()));
				if(index>1){
					sb.append(String.format(format,coeff.toString(),index));
				}
				if(it.hasNext()) sb.append(plus);
			}
			
			return sb.toString();
		}
	}
}
