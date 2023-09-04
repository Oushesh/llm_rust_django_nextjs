; ModuleID = 'probe7.74be8f4e-cgu.0'
source_filename = "probe7.74be8f4e-cgu.0"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128"
target triple = "arm64-apple-macosx11.0.0"

; core::f64::<impl f64>::to_ne_bytes
; Function Attrs: inlinehint uwtable
define internal i64 @"_ZN4core3f6421_$LT$impl$u20$f64$GT$11to_ne_bytes17h66d9b868391cf003E"(double %self) unnamed_addr #0 {
start:
  %0 = alloca i64, align 8
  %_3 = alloca double, align 8
  %1 = alloca [8 x i8], align 1
  store double %self, ptr %_3, align 8
  %rt = load double, ptr %_3, align 8, !noundef !1
  %2 = bitcast double %rt to i64
  store i64 %2, ptr %0, align 8
  %self1 = load i64, ptr %0, align 8, !noundef !1
  store i64 %self1, ptr %1, align 1
  %3 = load i64, ptr %1, align 1
  ret i64 %3
}

; probe7::probe
; Function Attrs: uwtable
define void @_ZN6probe75probe17h272abc9f4b731394E() unnamed_addr #1 {
start:
  %0 = alloca i64, align 8
  %_1 = alloca [8 x i8], align 1
; call core::f64::<impl f64>::to_ne_bytes
  %1 = call i64 @"_ZN4core3f6421_$LT$impl$u20$f64$GT$11to_ne_bytes17h66d9b868391cf003E"(double 3.140000e+00)
  store i64 %1, ptr %0, align 8
  call void @llvm.memcpy.p0.p0.i64(ptr align 1 %_1, ptr align 8 %0, i64 8, i1 false)
  ret void
}

; Function Attrs: argmemonly nocallback nofree nounwind willreturn
declare void @llvm.memcpy.p0.p0.i64(ptr noalias nocapture writeonly, ptr noalias nocapture readonly, i64, i1 immarg) #2

attributes #0 = { inlinehint uwtable "frame-pointer"="non-leaf" "target-cpu"="apple-a14" }
attributes #1 = { uwtable "frame-pointer"="non-leaf" "target-cpu"="apple-a14" }
attributes #2 = { argmemonly nocallback nofree nounwind willreturn }

!llvm.module.flags = !{!0}

!0 = !{i32 7, !"PIC Level", i32 2}
!1 = !{}
