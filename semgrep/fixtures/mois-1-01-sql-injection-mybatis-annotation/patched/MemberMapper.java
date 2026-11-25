package egovframework.member.service.impl;

import java.util.List;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface MemberMapper {
    String BASE_SELECT = "SELECT member_id, member_nm FROM tb_member";

    // ok: mois-1-01-sql-injection-mybatis-annotation — #{} 는 바인딩 변수
    @Select("SELECT member_id, member_nm FROM tb_member WHERE member_nm = #{memberNm}")
    List<MemberVO> selectByName(@Param("memberNm") String memberNm);

    @Select("SELECT member_id, member_nm FROM tb_member "
            + "ORDER BY member_id")
    List<MemberVO> selectAll();

    @Select(BASE_SELECT + " WHERE dept_id = #{deptId}")
    List<MemberVO> selectByDept(@Param("deptId") String deptId);

    @Update(value = "UPDATE tb_member SET member_nm = #{memberNm} WHERE member_id = #{memberId}")
    int updateName(@Param("memberId") long memberId, @Param("memberNm") String memberNm);

    // 정렬 기준은 바인딩할 수 없으므로 허용된 값만 분기로 고른다
    @Select({"<script>",
            "SELECT member_id, member_nm FROM tb_member",
            "<if test='keyword != null'>WHERE member_nm LIKE CONCAT('%', #{keyword}, '%')</if>",
            "<choose><when test=\"sortColumn == 'name'\">ORDER BY member_nm</when><otherwise>ORDER BY member_id</otherwise></choose>",
            "</script>"})
    List<MemberVO> search(@Param("keyword") String keyword, @Param("sortColumn") String sortColumn);

    @Insert("INSERT INTO tb_member (member_id, member_nm) VALUES (#{memberId}, #{memberNm})")
    int insert(@Param("memberId") long memberId, @Param("memberNm") String memberNm);

    // ok: mois-1-01-sql-injection-mybatis-annotation — 중괄호 없는 $ 는 치환이 아니다
    @Select("SELECT CONCAT('$', fee) FROM tb_member WHERE member_id = #{memberId}")
    String selectFee(@Param("memberId") long memberId);

    @Delete(value = {"DELETE FROM tb_member", "WHERE member_id = #{memberId}"})
    int delete(@Param("memberId") long memberId);
}
