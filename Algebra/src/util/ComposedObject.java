package util;
/**
 * A composed object: the first argument may be of different type as the
 * second argument
 * @author bzfmuell
 *
 * @param <K> type of first argument
 * @param <V> type of second argument
 */
public class ComposedObject<K, V> implements Cloneable {
	/**the first argument*/
	private K  first;
	/**the second argument*/
	private V second;
	/**
	 * Constructs a <code>ComposedObject</code> having
	 * parameter <tt>first</tt> as first argument and
	 * <tt>second</tt> as second argument
	 * @param first the first argument
	 * @param second the second argument
	 */
	public ComposedObject (K first, V second) {
		this.first  = first;
		this.second = second;
	}
	/**
	 * Clone constructor - clones the parameter
	 * <tt>another</tt>
	 * @param another some other composed object
	 */
	public ComposedObject (ComposedObject<K,V> another){this(another.first,another.second);}
	/**
	 * Returns a deep copy of this
	 */
	public ComposedObject<K,V> clone (){return new ComposedObject<K,V> (this);}
	/**
	 * Returns true if and only if first and second argument are
	 * equal - that is both objects are referring to the same object
	 * (<tt>this==o</tt> returns true), or the first and second objects
	 * are equal (same type as well as by their own <tt>equals()</tt> method)
	 */
	public boolean equals (Object o){
		if(this==o) return true;
		if(!(o instanceof ComposedObject)) return false;
		ComposedObject<?,?> cp = (ComposedObject<?,?>) o;
		if(!(getFirstClass().getName().matches(cp.getFirstClass().getName()))
				||!(getSecondClass().getName().matches(cp.getSecondClass().getName()))) return false;
		return cp.first.equals(first)&&cp.second.equals(second)?true:false;
	}
	/**
	 * Returns the type of the first argument
	 * @return the type
	 */
	public Class<?> getFirstClass (){return first.getClass();}
	/**
	 * Returns the type of the second argument
	 * @return the type
	 */
	public Class<?> getSecondClass (){return second.getClass();}
	/**
	 * Returns the first argument
	 * @return the first
	 */
	public K getFirst (){return first;}
	/**
	 * Returns the second argument
	 * @return the second
	 */
	public V getSecond(){return second;}
	public int hashCode (){return 17*first.hashCode()+37*second.hashCode();}
}
