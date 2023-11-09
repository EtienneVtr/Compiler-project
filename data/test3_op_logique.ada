with Ada.Text_IO; use Ada.Text_IO;
procedure ProgrammeAvecReverse is
   function Factorial(N: Integer) return Integer is
      Result : Integer := 1;
   begin
      for I in reverse 1..N loop
         Result := Result * I;
      end loop;
      return Result;
   end Factorial;

   function IsPrime(X: Integer) return Boolean is
   begin
      for I in 2..Integer'Sqrt(X) loop
         if X mod I = 0 then
            return false;
         end if;
      end loop;
      return true;
   end IsPrime;

begin
   null;
end ProgrammeAvecReverse;
