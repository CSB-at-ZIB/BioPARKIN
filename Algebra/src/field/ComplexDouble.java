package field;

import module.GenericVSpace;
import group.ComplexSphere;
/**
 * The class of double precision complex floating points: each complex
 * floating point is represented by its angle on the complex unit sphere S^1
 * and its radius (absolute value)
 * @author adin
 *
 */
public class ComplexDouble extends AbstractField<ComplexDouble> {
	private static final String FORMAT_STRING1 = "%1$s e^(2\u03c0 %2$s)";
	private static final String FORMAT_STRING2 = "%1$6g %3$s %2$6g i";
	private ComplexSphere angle;
	private DoubleField  radius;
	private boolean angularStringRep;
	public ComplexDouble() {this(0,0);}
	
	public ComplexDouble (double realPart, double imagPart){
		this(new ComplexSphere(Math.atan(imagPart/realPart)/(2*Math.PI)+realPart>=0&&imagPart>=0?0:realPart<0&&imagPart>=0?.25:realPart<0&&imagPart<0?.5:.75),
				Math.sqrt(realPart*realPart+imagPart*imagPart));
	}
	public ComplexDouble (DoubleField realPart, DoubleField imagPart){
		this(realPart.getValue(),imagPart.getValue());
	}
	public ComplexDouble(ComplexSphere angle, double radius){
		this(angle,new DoubleField(radius));
	}
	
	public ComplexDouble (ComplexSphere angle, DoubleField radius){
		super();
		if(radius.compareTo(DoubleField.ZERO)<0) radius = radius.addInverse();
		this.angle = angle;
		this.radius = radius;
		if(radius.compareTo(DoubleField.ZERO)>0) isZero = false;
		//angularStringRep = true;
	}
	
	public ComplexDouble inverse() {
		if(isZero()) throw new IllegalArgumentException ("\nZero division");
		return new ComplexDouble (new ComplexSphere(-angle.getPhi()),radius.multiply(radius).inverse());
	}

	
	public ComplexDouble addInverse() {
		GenericVSpace<DoubleField> v = getAsVector();
		DoubleField real = v.getValue(0), imag = v.getValue(1);
		if(real!=null&&imag!=null) return new ComplexDouble(real.addInverse(),imag.addInverse());
		if(real!=null&&imag==null) return new ComplexDouble(real.addInverse(),DoubleField.ZERO);
		if(real==null&&imag!=null) return new ComplexDouble(DoubleField.ZERO,imag.addInverse());
		return new ComplexDouble();
	}
	public boolean isZero() {return radius.isZero()?true:false;}

	
	public ComplexDouble multiply(ComplexDouble another) {
		return new ComplexDouble(angle.add(another.angle),radius.multiply(another.radius));
	}

	public double abs(){return radius.getValue();}
	
	public ComplexDouble add(ComplexDouble another) {
		GenericVSpace<DoubleField> v1 = getAsVector(), v2 = another.getAsVector();
		v1 = v1.add(v2);
		DoubleField val1 = v1.getValue(0), val2 = v1.getValue(1);
		if(val1!=null&&val2!=null) return new ComplexDouble(val1,val2);
		if(val1!=null&&val2==null) return new ComplexDouble(val1,DoubleField.ZERO);
		if(val1==null&&val2!=null) return new ComplexDouble(DoubleField.ZERO,val2);
		return new ComplexDouble();
		
	}
	
	public ComplexDouble constructOne(){return new ComplexDouble (1,0);}

	public ComplexSphere getAngle (){return angle;}
	
	public DoubleField getRadius (){return radius;}
	
	public GenericVSpace<DoubleField> getAsVector(){
		GenericVSpace<DoubleField> complexVec  = new GenericVSpace<DoubleField>();
		if(angle.equals(ComplexSphere.NEUTRAL)){
			complexVec.setEntry(0, radius);
			return complexVec;
		}
		if(angle.equals(ComplexSphere.HALF)){
			complexVec.setEntry(0, DoubleField.M_ONE.multiply(radius));
			return complexVec;
		}
		if(angle.equals(ComplexSphere.QUARTER)){
			complexVec.setEntry(1, radius);
			return complexVec;
		}
		if(angle.equals(ComplexSphere.THREE_QUARTER)){
			complexVec.setEntry(1, DoubleField.M_ONE.multiply(radius));
			return complexVec;
		}
		double phi = 2*Math.PI*angle.getPhi();
		complexVec.setEntry(0, radius.multiply(new DoubleField(Math.cos(phi))));
		complexVec.setEntry(1, radius.multiply(new DoubleField(Math.sin(phi))));
		return complexVec;
	}
	
	public boolean equals(ComplexDouble another) {
		if(this==another)return true;
		if(Math.abs(radius.add(another.radius.addInverse()).getValue())<5e-16&&angle.equals(another.angle)) return true;
		return false;
	}

	
	public String toString (){
		if(isZero()) return "0";
		boolean neutral;
		if((neutral = angle.equals(ComplexSphere.NEUTRAL))||angle.equals(ComplexSphere.HALF)) return String.format("%1$6g",neutral?radius.getValue():-radius.getValue());
		boolean quart;
		if((quart = angle.equals(ComplexSphere.QUARTER))||angle.equals(ComplexSphere.THREE_QUARTER)) return String.format("%1$6g i", quart?radius.getValue():-radius.getValue());
		if(angularStringRep){
			return String.format(FORMAT_STRING1, radius.toString(),""+angle.getPhi());
		}
		double phi = 2*Math.PI*angle.getPhi(), rad = radius.getValue(), sin = rad*Math.sin(phi);
		return String.format(FORMAT_STRING2, rad*Math.cos(phi),sin<0?-sin:sin,sin<0?"-":"+");
	}
	public static void main(String[] args){
		/*System.out.println(""+(-1.2%1.0));
		double sqrt3 = .5*Math.sqrt(3);
		ComplexDouble z1 = new ComplexDouble(-.5,-sqrt3), z2 = new ComplexDouble(-.5,sqrt3);
		System.out.println(String.format("%1$s + %2$s = %3$s",z1.toString(),z2.toString(),z1.add(z2).toString()));
		System.out.println(String.format("%1$s - %2$s = %3$s",z1.toString(),z2.toString(),z1.add(z2.addInverse()).toString()));*/
		double phi = 0;
		while (phi<1.01){
			System.out.println(String.format("e^(2 pi i * %1$g) = %2$s",phi,new ComplexDouble(new ComplexSphere(phi),1)));
			phi += .01;
		}
	}
}
