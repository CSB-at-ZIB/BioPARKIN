package util;
/**
 * An utility class: implements all the basic methods of the {@link Function}
 * interface. The only method left to implement is {@link Function#f()}. For
 * convenience, two instance variables are provided:
 * <br /><br />
 * <ol><li>the independent variable <code>x</code> or argument of some reference type <code>X</code></li>
 * <li>the dependent variable <code>y</code> or image of some reference type <code>Y</code></li></ol>  
 * @author adin
 *
 * @param <X> the type of the argument
 * @param <Y> the type of the image
 */
public abstract class AbstractFunction<X, Y> implements Function<X, Y> {
	/**the argument*/
	protected X x;
	/**the image*/
	protected Y y;
	/**
	 * Constructs an empty function object
	 */
	public AbstractFunction() {}
	
	public void f(X arg) {
		if(arg==null) return;
		x = arg;
		f();
	}

	
	public X getArgument() {return x;}

	
	public Y getValue() {return y;}
	/**
	 * Sets the argument to <tt>x</tt> if
	 * <code>x!=null</code> returns true
	 * @param x the argument (not null)
	 */
	public void setArgument(X x){
		if(x!=null) this.x = x;
	}
}
