package homomorphism;

import ring.Ring;
import group.AbstractAbel;
/**
 * The generic ring homomorphism class: three methods need to be implemented by any sub class
 * <ol><li>{@link GenericRingHomo#equals(group.Monoid)} - a comparison method similar to <code>Object.equals(Object)</code></li>
 * <li>{@link GenericRingHomo#f() } - the evaluation method: computes the image <tt>f(arg)</tt> of the current argument <tt>arg</tt></li>
 * <li>{@link GenericRingHomo#isZero()} - must return true, if <tt>getValue().isZero()</tt> returns true for all arguments <tt>arg in R</tt>
 * </ol>
 * @author bzfmuell
 *
 * @param <R> the preimage type
 * @param <S> the image type
 */
public abstract class GenericRingHomo<R extends Ring<R>,S extends Ring<S>> extends AbstractAbel<GenericRingHomo<R,S>>implements RingHomo<GenericRingHomo<R,S>,R,S>{
	/**the argument value*/
	protected R arg;
	/**the image value*/
	protected S val;
	/**
	 * Constructs the empty homomorphism
	 */
	public GenericRingHomo (){super();}
	
	public GenericRingHomo<R, S> add(GenericRingHomo<R, S> another) {
		final GenericRingHomo<R,S> tHomo = this;
		final GenericRingHomo<R,S> aHomo = another;
		return new GenericRingHomo<R,S> (){

			public void f() {
				tHomo.f(arg);
				aHomo.f(arg);
				val = tHomo.val.add(aHomo.val);
			}

			public boolean equals(GenericRingHomo<R, S> another) {return add(another.addInverse()).isZero()?true:false;}
			
			public boolean isZero() {return tHomo.add(aHomo).isZero()?true:false;}


			
		};

	}

	public GenericRingHomo<R, S> addInverse() {
		final GenericRingHomo<R,S> tHomo = this;
		return new GenericRingHomo<R,S> (){

			public void f() {tHomo.f(arg);val = tHomo.val.addInverse();}
			
			public boolean equals (GenericRingHomo<R,S> another){return add(another.addInverse()).isZero()?true:false;}
			
			public boolean isZero (){return tHomo.isZero()?true:false;}
		};
	}

	
	public void f(R arg){
		this.arg = arg;
		f();
	}
	public R getArgument() {return arg==null?null:arg;}
	
	public S getValue() {if(val==null&&arg!=null) f();return val==null?null:val;}
	
	public boolean isCommutative (){
		if(isZero()||arg==null) return true;
		if(arg!=null)f();
		return val.isCommutative()?true:false;		 
	}

	public GenericRingHomo<R, S> multiply(GenericRingHomo<R, S> another) {
		final GenericRingHomo<R,S> tHomo = this;
		final GenericRingHomo<R,S> aHomo = another;
		return new GenericRingHomo<R,S> (){

			public void f() {
				tHomo.f(arg);
				aHomo.f(arg);
				val = tHomo.val.multiply(aHomo.val);
			}

			public boolean equals(GenericRingHomo<R, S> another) {return add(another.addInverse()).isZero()?true:false;}
			
			public boolean isZero() {return tHomo.multiply(aHomo).isZero()?true:false;}


			
		};
	}
	
	public void setArgument(R arg) {this.arg = arg;}

		

	
}
