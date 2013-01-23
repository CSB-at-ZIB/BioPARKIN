package util;
/**
 * The parameterized function interface
 * @author gmueller
 *
 * @param <X> the argument type
 * @param <Y> the image value type 
 */
public interface Function<X,Y> {
	/**
	 * Computes the value of the
	 * current argument
	 */
	public void f();
	/**
	 * Computes the value of the
	 * given argument <tt>arg</tt>
	 * @param arg the argument
	 */
	public void f(X arg);
	/**
	 * Returns the current argument
	 * @return the argument
	 */
	public X getArgument ();
	/**
	 * Returns the image value <tt>f(arg)</tt>,
	 * where <tt>arg</tt> is the current argument
	 * @return the image
	 */
	public Y getValue ();
}
