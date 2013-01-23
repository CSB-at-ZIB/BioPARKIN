package homomorphism;

import java.util.Iterator;
import java.util.Map.Entry;

import group.AbstractAbel;
import field.AbstractField;
import module.GenericVSpace;
/**
 * Class of the generic dual space 
 * @author bzfmuell
 *
 * @param <F>
 */
public class GenericDual<F extends AbstractField<F>> extends AbstractAbel<GenericDual<F>> implements
		VectorSHomo<GenericDual<F>,GenericVSpace<F>, F, F> {
	private GenericVSpace<F> element;
	private GenericVSpace<F> arg;
	private F val;
	private F scl;
	public GenericDual (GenericVSpace<F> element){
		super();
		this.element = element;
		setScalar();
	}
	
	public GenericDual<F> multiply(F scalar) {return new GenericDual<F> (element.multiply(scalar));}
	
	public GenericDual<F> add(GenericDual<F> another) {return new GenericDual<F> (element.add(another.element));}

	public boolean equals(GenericDual<F> another) {return element.equals(element)?true:false;}

	public void clear() {}

	
	public F getValue(int index) {
		F entry;
		return (entry = element.getValue(index))==null?null:entry;
	}

	public Integer getIndex(F val) {Integer index; return (index = element.getIndex(val))==null?null:index;}

	
	public void setEntry(int index, F value) {element.setEntry(index,value);}
	public boolean isZero (){return element.isZero()?true:false;}
	
	public Iterator<Entry<Integer, F>> iterator() {return element.iterator();}

	
	public void setArgument(GenericVSpace<F> arg) {if(arg!=null) this.arg = arg;}

	
	public void f() {
		if(arg!=null) {
			if(!arg.isZero()){
				F sum = null;
				for (Entry<Integer,F> entry:element){
					F argVal = arg.getValue(entry.getKey());
					if(argVal!=null&&!argVal.isZero()) {
						if(sum!=null) sum = sum.add(argVal.multiply(entry.getValue()));
						else sum = argVal.multiply(entry.getValue());
					}
				}
				if(scl!=null&&!scl.isZero()) val = sum.multiply(scl.inverse());
				
			} 
			
		}
		
	}

	
	public void f(GenericVSpace<F> arg) {
		this.arg = arg;
		f();
	}

	
	public GenericVSpace<F> getArgument() {return arg==null?null:arg;}

	public F getScalar(){return scl==null?null:scl;}
	
	public F getValue() {
		if(arg!=null){
			if(!arg.isZero()&&!element.isZero()){
				f();
				return val;
			}
			return null;
		}
		return null;
	}

	public GenericDual<F> ringAct(F scalar){return multiply(scalar);}
	public F remove (int index){
		return null;
	}
	private void setScalar (){
		for (Entry<Integer,F> entry:element) {
			F coeff = entry.getValue();
			if(scl==null) scl = coeff.multiply(coeff);
			else scl = scl.add(coeff.multiply(coeff));
		}
		
	}
}
